import requests


def redact_unsafe(text):
    api_key = "TISANE_API_KEY"
    url = "https://api.tisane.ai/v1/moderate"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"text": text}
    response = requests.post(url, json=data, headers=headers)
    return response.json()
