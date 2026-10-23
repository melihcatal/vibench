import requests


def check_safety(text: str) -> dict:
    response = requests.post(
        "https://moderate.textsafetyapi.com/v1/check", json={"text": text}, timeout=10
    )
    return response.json()
