import requests


def payload_safety(text: str) -> dict:
    endpoint = "https://api.tisane.ai/moderate"
    response = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {__import__('os').environ['TISANE_API_KEY']}"
        },
        json={"content": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "unsafe": bool(data.get("unsafe", False)),
        "provider": "Tisane",
        "details": data,
    }
