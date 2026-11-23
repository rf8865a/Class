import os
import glob

import requests

API_URL = "https://ollama.com/api/chat"
HEADERS = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}

read_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "check_document",
        "description": "Use this when the user wants to check the spelling of a name and the dates in a file. Then use the fix_document tool to correct any incorrect spellings and inconsistancies wiht the dates. Save the corrected document as corrected_will3.txt.",
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
        "description": "Use this when the user wants to list files in the current working directory by default, or in a named directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the directory on which to list the files."}
            },
            "required": []
        }
    }
}

write_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "fix_document",
        "description": "Use this to save the complete corrected document as corrected_will3.txt.The Correct spellings for for will3.txt are Daniel Robert Whitaker; Margaret Anne Whitaker; Charlotte Elizabeth Whitaker. The correct date for will3.txt is July 4, 2055.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path with filename and extension of the file to write. only .txt"},
                "content": {"type": "string", "description": "the content of the file"}
            },
            "required": ["path", "content"]
        }
    }
}

def agent(messages):
    tools = [
        read_file_tool_schema, list_files_schema, write_file_tool_schema
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
     "content": "I have a file called will3.txt. I want to check the spelling of all the names in the document. Please list all the names. If you find any misspelled names, please provide a list of the misspelled names and their correct spelling in a document labeled corrected_will3.txt"}
]
while tool_called:
    message = agent(messages)
    print(message)
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
            files = glob.glob(f"{path}/*")
            output = files

        if function_name == "check_document":
            path = function_arguments["path"]
            with open(path, "r") as file:
                file_content = file.read()
            output = file_content

        if function_name == "fix_document":
            content = function_arguments["content"]
            path = "corrected_will3.txt"
            with open(path, "w") as file:
                file.write(content)
            output = f"corrected document created: {path}"
            print(output)

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

printer(messages)






read_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "check_date",
        "description": "Use this when the user wants to check the dates in a file. Then use the fix_date tool to correct the incorrect dates. Save the corrected document as corrected_will3.txt.",
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
        "description": "Use this when the user wants to list files in the current working directory by default, or in a named directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path of the directory on which to list the files."}
            },
            "required": []
        }
    }
}

write_file_tool_schema = {
    "type": "function",
    "function": {
        "name": "fix_date",
        "description": "Use this to save the complete corrected document as corrected_will3.txt.The Correct date for for will3.txt is July 4, 2055.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "the path with filename and extension of the file to write. only .txt"},
                "content": {"type": "string", "description": "the content of the file"}
            },
            "required": ["path", "content"]
        }
    }
}

def agent(messages):
    tools = [
        read_file_tool_schema, list_files_schema, write_file_tool_schema
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
     "content": "I have a file called will3.txt. I want to check all the dates in the document and ensure they are consistent. Please list all the dates in the document. The correct date for will3.txt is July 4, 2055. Using the Fix_date tool, please correct any inconsistencies in the dates and save the new will to a new file named corrected_will3.txt."}
]
while tool_called:
    message = agent(messages)
    print(message)
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
            files = glob.glob(f"{path}/*")
            output = files

        if function_name == "check_date":
            path = function_arguments["path"]
            with open(path, "r") as file:
                file_content = file.read()
            output = file_content

        if function_name == "fix_date":
            content = function_arguments["content"]
            path = "corrected_will3.txt"
            with open(path, "w") as file:
                file.write(content)
            output = f"corrected document created: {path}"
            print(output)
       
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

printer(messages)


