import requests

def chat_with_gpt(prompt):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-3.5-turbo",  # Use the appropriate model
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

prompt = "How much do elephants weigh"  # Example user input
response = chat_with_gpt(prompt)
print(response)