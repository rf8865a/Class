import os

import requests

API_URL = "https://ollama.com/api/chat"
HEADERS = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}

tool_schema = {
    "type": "function",
    "function": {
        "name": "add2",
        "description": "Use when the user asks for the weather forecast in a location.",
        "parameters": {
            "type": "object",
            "properties": {
                "arg1": {"type": "string", "description": "The location from which we want the weather"},
                 
            },
            "required": ["arg1"]
        }
    }
}
list_files_schema = {
      "type": "function",
      "function": {
            "name": "list_files", 
            "description": "use this when the user wants to list files in the current dictonary", 
            "parameters": {
                  "type": "object",
                  "properties": {},
                  "required": []
            }
      }
}

def agent(messages):
    payload = {
        "model": "gpt-oss:120b",
        "messages": messages,
        "stream": False,
    }
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=300,
        "tools": tools 
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]

tool_called = True
messages = [{"role": "user", "content": "what are the files in the current directory"}]
while tool_called:
    message = agent(messages)
    tool_called = "tool_calls" in message

   if tool_called:
        pass
    else: 
     ai_message = {
          "role": 
     }


import pprint
printer = pprint.pprint
printer(message)

with open("messages.txt", "w") as file:
          file.write(printer(messages))

          if function_name =="list_files":
                path = "."
                files = "\n".join