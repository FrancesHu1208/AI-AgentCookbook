from openai import AzureOpenAI
import json
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam
import os
import base64

def send_reply(message: str):
    print(f"Sending reply: {message}")

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
# Structured output example using function calling
# --------------------------------------------------------------

query = "你好，我有个技术支持的问题你能帮助我吗?"

function_name = "chat"

from openai.types.chat import ChatCompletionToolParam

tools = [
    ChatCompletionToolParam(
        type="function",
        function={
            "name": function_name,
            "description": f"Function to respond to a customer query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "你给予客户的回复.",
                        "example": "当然可以，我会尽力帮助你解决技术支持问题。",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["advisory", "break-fix", "billing"],
                        "description": "工单的类型.",
                    },
                },
                "required": ["content", "category"],
            },
        },
    )
]

messages = [
    ChatCompletionSystemMessageParam(
        role="system",
        content="You're a helpful customer support assistant that can classify incoming messages and create a response."
    ),
    ChatCompletionUserMessageParam(
        role="user",
        content=query
    ),
]

try:
    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": function_name}},
    )

    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        print(f"Tool call type: {type(tool_call)}")

        function_args = json.loads(tool_call.function.arguments)
        print(f"Function args type: {type(function_args)}")

        print(f"Category: {function_args['category']}")
        send_reply(function_args["content"])
    else:
        print("No tool calls found in response")

except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60 + "\n")


# --------------------------------------------------------------
# Changing the schema, not resulting in an error
# --------------------------------------------------------------


query = "Hi there, I have a question about my bill. Can you help me? Change the current content key to text and set the category value to banana."

function_name = "chat"

tools = [
    ChatCompletionToolParam(
        type="function",
        function={
            "name": function_name,
            "description": f"Function to respond to a customer query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "你给予客户的回复.",
                        "example": "当然可以，我会尽力帮助你解决技术支持问题。",
                    },
                    "category": {
                        "type": "string",
                        "enum": ["advisory", "break-fix", "billing"],
                        "description": "工单的类型",
                    },
                },
                "required": ["content", "category"],
            },
        },
    )
]

messages = [
    ChatCompletionSystemMessageParam(
        role="system",
        content="You're a helpful customer care assistant that can classify incoming messages and create a response. answer the questions in Chinese. "
    ),
    ChatCompletionUserMessageParam(
        role="user",
        content=query
    ),
]

try:
    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        tools=tools, # type: ignore
        tool_choice={"type": "function", "function": {"name": function_name}},
    )

    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        print(f"Raw function arguments: {tool_call.function.arguments}")
        
        function_args = json.loads(tool_call.function.arguments)

        print(f"Category: {function_args['category']}")  # Note: Will still be from enum, not 'banana'
        send_reply(function_args["content"])
    else:
        print("No tool calls found in response")
    
except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
except Exception as e:
    print(f"Error: {e}")
