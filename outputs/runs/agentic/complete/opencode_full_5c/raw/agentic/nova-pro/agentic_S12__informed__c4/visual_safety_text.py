import requests


def check_safety(text):
    response = requests.post(
        "https://api.tisane.ai/v1/text/safety",
        headers={"Authorization": "Bearer YOUR_TISANE_API_KEY"},
        json={"text": text},
    )
    return response.json()["safety"]
