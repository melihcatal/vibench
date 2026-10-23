import requests


def embed_script(text):
    api_key = "YOUR_TISANE_API_KEY"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"text": text}
    response = requests.post(
        "https://api.tisane.com/v1/embed", headers=headers, json=data
    )
    return response.json().get("embedding")
