import os
import glob 
import subprocess

import requests

API_URL = "https://ollama.com/api/chat"
HEADERS = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}

read_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Use this when the user wants to read a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the file to read"},
            },
            "required": ["path"]
        }
    }
}

list_files_schema = {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "Use this when the user wants to list files in the current working directory, or in a named directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the directory to list files in"}
            },
            "required": []
        }
    }
}

write_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Use this when the user wants to write to a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path with filename and extension of the file to write. only .txt"},
                "content": {"type": "string", "description": "the content of thefile"}
            },
            "required": ["path", "content"]
        }
    }
}

run_python_schema = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Use this when the user wants to run a python file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the python file to run"}
            },
            "required": ["path"]
        }
    }
}




def agent(messages):
    tools = [
        read_file_tool_schema, list_files_schema, write_file_tool_schema, run_python_schema
    ]

    payload = {
        "model": "gpt-oss:120b",
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
     "content": "write fizzbuzz in python in a file called robot fizzbuzz."}
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
            if "path" in function_arguments:
                path = function_arguments["path"]
            print(f"arguments for list_files: {path}")
            #files = /n.join(os.listdir(path))
            files = glob.glob(f"{path}/*")
            output = f"The output of {function_name} is: {files}"

        if function_name == "read_file":
            path = function_arguments["path"]
            with open(path, "r") as file:
                file_content = file.read()
            output = f"The output of {function_name} is: {file_content}"

        if function_name == "write_file":
            path = function_arguments["path"]
            content = function_arguments["content"]
            with open(path, "w") as file:
                file.write(content)
            output = f"File written to {path} with content: {content}"
      
    
        if function_name == "run_python_file":
            path = function_arguments["path"]
            import subprocess
            result = subprocess.run(["python", path], capture_output=True, text=True)
            output = f"The output of python {path} is: {result.stdout}"
           
            
        
        
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

