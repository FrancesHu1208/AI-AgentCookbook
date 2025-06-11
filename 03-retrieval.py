# %%
import json
import os

from openai import AzureOpenAI
from pydantic import BaseModel, Field

"""
docs: https://platform.openai.com/docs/guides/function-calling
"""
# %%

endpoint = os.getenv("ENDPOINT_URL", "https://<endpoint>.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1")
api_key = os.getenv("AZURE_API_KEY")


# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2025-01-01-preview",
)


# --------------------------------------------------------------
# Define the knowledge base retrieval tool
# --------------------------------------------------------------




def search_kb(question: str):
    """
    Load the whole knowledge base from the JSON file.
    (This is a mock function for demonstration purposes, we don't search)
    """
    with open("kb.json", "r") as f:
        return json.load(f)


# --------------------------------------------------------------
# Step 1: Call model with search_kb tool defined
# --------------------------------------------------------------
# %%

kbtools = [
    {
        "type": "function",
        "function": {
            "name": "search_kb",
            "description": "Get the answer to the user's question from the knowledge base.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                },
                "required": ["question"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]
# %%
system_prompt = "You are a helpful assistant that answers questions from the knowledge base about our e-commerce store."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is the return policy?"},
]

# %%
completion = client.chat.completions.create(
    model=deployment,
    messages=messages, # type: ignore
    tools=kbtools, # type: ignore
)



print("First time, LLM didn't call tool:", completion.choices[0].message.content)
print("Print model dump information:", completion.model_dump())

# %%

# --------------------------------------------------------------
# Step 2: Model decides to call function(s)
# --------------------------------------------------------------

# %%

# --------------------------------------------------------------
# Step 3: Execute search_kb function
# --------------------------------------------------------------


def call_function(name, args):
    if name == "search_kb":
        return search_kb(**args)


# 遍历 completion.choices[0].message.tool_calls 中的每个工具调用
for tool_call in completion.choices[0].message.tool_calls: # type: ignore
    # 获取工具调用的函数名
    name = tool_call.function.name
    # 解析工具调用的参数（JSON字符串转为Python对象）
    args = json.loads(tool_call.function.arguments)
    # 将当前消息追加到 messages 列表
    messages.append(completion.choices[0].message) # type: ignore

    # 调用对应的函数，并获取结果
    result = call_function(name, args)
    # 将工具调用的结果以特定格式追加到 messages 列表
    messages.append(
        {
            "role": "tool",  # 标记为工具角色
            "tool_call_id": tool_call.id,  # 工具调用的唯一标识
            "content": json.dumps(result)  # 结果序列化为 JSON 字符串
        }
    )

print("print information read from KB", json.dumps(result)) # type: ignore
# --------------------------------------------------------------
# Step 4: Supply result and call model again
# --------------------------------------------------------------
# %%

class KBResponse(BaseModel):
    answer: str = Field(description="The answer to the user's question.")
    source: int = Field(description="The record id of the answer.")


completion_2 = client.beta.chat.completions.parse(
    model=deployment,
    messages=messages, # type: ignore
    tools=kbtools, # type: ignore
    response_format=KBResponse,
)

# --------------------------------------------------------------
# Step 5: Check model response
# --------------------------------------------------------------

final_response = completion_2.choices[0].message.parsed
final_response.answer # type: ignore
final_response.source # type: ignore
print("final answer:", final_response)
# %%
# --------------------------------------------------------------
# Question that doesn't trigger the tool
# --------------------------------------------------------------

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is the weather in Tokyo?"},
]

completion_3 = client.beta.chat.completions.parse(
    model=deployment,
    messages=messages, # type: ignore
    tools=kbtools, # type: ignore
)

completion_3.choices[0].message.content
print("question that doesn't trigger the tool:", completion_3.choices[0].message.content)

# %%
