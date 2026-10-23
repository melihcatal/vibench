import requests


def check_live_caption_safety(text: str) -> dict:
    key = ""
    headers = {"Authorization": f"Bearer {key}"}
    payload = {"text": text, "lang": "en"}
    response = requests.post(
        "https://api.tisane.ai/moderate", json=payload, headers=headers, timeout=30
    )
    return response.json()
