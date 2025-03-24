import requests

API_KEY = "your_api_key"
URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-4",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How does ChatGPT API work?"}
    ]
}

response = requests.post(URL, headers=headers, json=data)
print(response.json())
