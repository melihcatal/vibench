import requests


def secret_label_safety(text):
    response = requests.post(
        "https://api.tisane.ai/moderate",
        headers={"X-Api-Key": __import__("os").environ.get("TISANE_API_KEY", "")},
        json={"content": text},
        timeout=30,
    )
    return response.json()
