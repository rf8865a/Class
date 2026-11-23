import os

import requests

API_URL = "https://ollama.com/api/chat"
HEADERS = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}

tool_schema = {
    "type": "function",
    "function": {
        "name": "add2",
        "description": "Use this when the user wants to add two numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "arg1": {"type": "string", "description": "the first number to add"},
                "arg2": {"type": "string", "description": "the second number to add"}
            },
            "required": ["arg1", "arg2"]
        }
    }
}

list_files_schema = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "Use this when the user wants to list files in the current working directory.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

def agent(messages):
    tools = [
        tool_schema, list_files_schema
    ]

    payload = {
        "model": "gpt-oss:20b",
        "messages": messages,
        "stream": False,
        "tools": tools
    }
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()
    message = data["message"]
    return message

tool_called = True
messages = [
    {"role": "user", 
     "content": "given these files find any errors in the spelling of the names and incorrect dates."}
]
while tool_called:
    message = agent(messages)
    tool_called = "tool_calls" in message

    if tool_called:
        print("tool called!")
        tool_calls = message["tool_calls"]
        tool_call = tool_calls[0]

        function_name = tool_call["function"]["name"]
        function_arguments = tool_call["function"]["arguments"]

        if function_name == "list_files":
            path = "."
            files = "\n".join(os.listdir(path))
            output = f"The output of {function_name} is: {files}"

        if function_name == "add2":
            arg1 = int(function_arguments["arg1"])
            arg2 = int(function_arguments["arg2"])
            print(f"function_name: {function_name}")
            print(f"arg1: {arg1}")
            print(f"arg2: {arg2}")

            output = arg1 + arg2
        tool_message = {
            "role": "tool",
            "content": f"The output of tool {function_name} is: {output}"
        }
        messages.append(tool_message)
    else:
        ai_message = {
            "role":  message["role"],
            "content": message["content"]
        }
        messages.append(ai_message)

last_message = messages[-1]
import pprint
printer = pprint.pprint
# printer(last_message)

printer(messages)
import base64with open("calculator/images.jpeg", "rb") as f:
    image_data = f.read()
image_base64 = base64.b64encode(image_data).decode("utf-8")

