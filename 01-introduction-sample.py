from openai import AzureOpenAI
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam
import os
import base64
import json


def send_reply(message: str):
    print(f"Sending reply: {message}")


endpoint = os.getenv("ENDPOINT_URL", "https://endpoint.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4.1")
api_key = os.getenv("AZURE_API_KEY") 

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2025-01-01-preview",
)

# --------------------------------------------------------------
# Unstructured output example
# --------------------------------------------------------------

query = "Hi there, I have a question about my bill. Can you help me?"

# Prepare the chat prompt
chat_prompt = [
    ChatCompletionSystemMessageParam(
        role="system", 
        content="You're a helpful customer care assistant"
    ),
    ChatCompletionUserMessageParam(
        role="user", 
        content=query
    ),
]

# Generate the completion
completion = client.chat.completions.create(
    model=deployment,
    messages=chat_prompt,
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
)

message = completion.choices[0].message.content
print(f"Unstructured response type: {type(message)}")
send_reply(message) # type: ignore

print("\n" + "="*60 + "\n")

# --------------------------------------------------------------
# Structured output example via prompt engineering
# --------------------------------------------------------------

query = "Hi there, I have a question about my bill. Can you help me?"

messages = [
    {
        "role": "system",
        "content": """
        You're a helpful customer care assistant that can classify incoming messages and create a response.
        Always response in the following JSON format: {"content": <response>, "category": <classification>}
        Available categories: 'general', 'order', 'billing'
        """,
    },
    {
        "role": "user",
        "content": query,
    },
]

completion = client.chat.completions.create(
    model=deployment,
    messages=messages, # type: ignore
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
) # type: ignore

message = completion.choices[0].message.content
print(f"Raw response type: {type(message)}")
print(f"Raw response: {message}")

try:
    message_dict = json.loads(message)
    print(f"Parsed response type: {type(message_dict)}")
    print(f"Response keys: {list(message_dict.keys())}")
    print(f"Content: {message_dict['content']}")
    print(f"Category: {message_dict['category']}")
    send_reply(message_dict["content"])
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    print(f"Raw message: {message}")

print("\n" + "="*60 + "\n")

# --------------------------------------------------------------
# Forcing structured output with response_format
# --------------------------------------------------------------

query = """
Hi there, I have a question about my bill. Can you help me? 
Don't reply with JSON, but output a single text string with your answer. 
"""

messages = [
    {
        "role": "system",
        "content": """
        You're a helpful customer care assistant that can classify incoming messages and create a response.
        Always response in the following JSON format: {"content": <response>, "category": <classification>}
        Available categories: 'general', 'order', 'billing'
        """,
    },
    {
        "role": "user",
        "content": query,
    },
]

completion = client.chat.completions.create(
    model=deployment,
    messages=messages, # type: ignore
    response_format={"type": "json_object"},
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False
) # type: ignore

# Fix: Access the message content correctly
message = completion.choices[0].message.content
print(f"Forced JSON response: {message}")

try:
    message_dict = json.loads(message)
    print(f"Content: {message_dict.get('content', 'N/A')}")
    print(f"Category: {message_dict.get('category', 'N/A')}")
    send_reply(message_dict.get("content", "No content available"))
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    print(f"Raw message: {message}")