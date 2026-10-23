import requests


def log_text_safety(text):
    endpoint = "https://api.openai.com/v1/moderations"
    response = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {__import__('os').getenv('OPENAI_API_KEY', '')}"
        },
        json={"model": "omni-moderation-latest", "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
