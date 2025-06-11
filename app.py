from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI
import json
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionSystemMessageParam, ChatCompletionToolParam
import os
from datetime import datetime

app = Flask(__name__)

# Initialize Azure OpenAI client
endpoint = os.getenv("ENDPOINT_URL", "https://ai-<endpoint>.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4")
api_key = os.getenv("AZURE_API_KEY")

if not api_key:
    print("Warning: AZURE_API_KEY environment variable not set!")
    print("Please set your Azure OpenAI API key in the environment variables.")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2025-01-01-preview",
)

def classify_and_respond(query, language="English"):
    """
    Classify user query and generate response using function calling
    """
    function_name = "chat"
    
    # Adjust descriptions based on language
    if language.lower() == "chinese":
        content_description = "你给予客户的回复."
        category_description = "工单的类型."
        system_content = "You're a helpful customer care assistant that can classify incoming messages and create a response. Answer the questions in Chinese."
    else:
        content_description = "Your reply that we send to the customer."
        category_description = "Category of the ticket."
        system_content = "You're a helpful customer care assistant that can classify incoming messages and create a response."
    
    tools = [
        ChatCompletionToolParam(
            type="function",
            function={
                "name": function_name,
                "description": "Function to respond to a customer query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": content_description,
                        },
                        "category": {
                            "type": "string",
                            "enum": ["advisory", "break-fix", "billing"],
                            "description": category_description,
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
            content=system_content
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
            function_args = json.loads(tool_call.function.arguments)
            
            return {
                "success": True,
                "content": function_args["content"],
                "category": function_args["category"],
                "raw_response": tool_call.function.arguments,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return {
                "success": False,
                "error": "No tool calls found in response"
            }
            
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON decode error: {e}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error: {e}"
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/classify', methods=['POST'])
def classify():
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "No query provided"}), 400
    
    query = data['query']
    language = data.get('language', 'English')
    
    if not query.strip():
        return jsonify({"error": "Query cannot be empty"}), 400
    
    result = classify_and_respond(query, language)
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    print("🚀 Starting AI Customer Care Assistant Web Interface...")
    print(f"📡 Endpoint: {endpoint}")
    print(f"🤖 Model: {deployment}")
    print(f"🔑 API Key: {'✅ Set' if api_key else '❌ Not Set'}")
    print("🌐 Server will be available at: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
