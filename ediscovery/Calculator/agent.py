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

def agent(messages):
    tools = [
        tool_schema
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
    

    import pprint 
    printer = pprint.pprint
    printer(data)

    message = data["message"]

    if "tool_calls" in message:
        print("we got a tool call!")
        tool_calls = message["tool_calls"]
        tool_call = tool_calls[0]
        printer(tool_call)
        
        function_name = tool_call["function"]["name"]
        function_arguments = tool_call["function"]["arguments"]

        if function_name == "add2":
         arg1 = function_arguments ["arg1"]
         arg2 = function_arguments["arg2"]
         print(f"function_name: {function_name}")
         print(f"arg1: {arg1}")
         print(f"arg2: {arg2}")

         output = arg1 + arg2
         print(output)

         if function_name == "get_weather":
            ...
    
    else:
        print("womp womp, no tool call.")

    return data ["message"]["content"]

messages = [{"role": "user", "content": "what is 100+ 5?."}]
print(agent(messages))
