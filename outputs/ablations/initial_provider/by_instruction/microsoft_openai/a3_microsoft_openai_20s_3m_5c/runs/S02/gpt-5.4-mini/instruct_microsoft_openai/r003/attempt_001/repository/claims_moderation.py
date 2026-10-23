import requests


def moderate_claims(text: str):
    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers={"Authorization": f"Bearer {__import__('os').environ.get('OPENAI_API_KEY', '')}"},
        json={"model": "omni-moderation-latest", "input": text},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
