# import os

# api_key = os.environ["OLLAMA_API_KEY"]

# print(api_key)

import os

import requests

with open("deposition.txt", "r") as file:
    contents = file.read()

prompt = f"""
At the end of this prompt I am inclduing the text of a case

please draft a case brief. 

here is the case:

{contents}
"""

api_url = "https://ollama.com/api/chat"
headers = {"Authorization": "Bearer " + os.environ["OLLAMA_API_KEY"]}
payload = {
    "model": "gpt-oss:120b",
    "messages": [
        {"role": "user", "content": prompt},
    ],
    "stream": False,
}

response = requests.post(
    api_url,
    headers=headers,
    json=payload,
)
response.raise_for_status()
data = response.json()

print(data["message"]["content"])


