import requests

def check_safety(text):
    api_key = "YOUR_TISANE_API_KEY"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post("https://api.tisane.ai/v1/text/safety", headers=headers, json={"text": text})
    return response.json()