import requests


def claims_moderation(payload, config=None):
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"},
        json={"model": "omni-moderation-latest", "input": payload["text"]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
