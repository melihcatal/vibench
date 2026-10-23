import requests


def claims_moderation(text: str):
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={"Authorization": "Bearer ", "Content-Type": "application/json"},
        json={"model": "omni-moderation-latest", "input": text},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()
