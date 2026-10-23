import os

import requests


def moderation_summary(payload, config=None):
    prompt = payload["text"] if isinstance(payload, dict) else str(payload)
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {((config or {}).get('api_key') or os.environ['OPENAI_API_KEY'])}", "Content-Type": "application/json"},
        json={"model": "gpt-5.4-mini", "input": f"Summarize moderation decision: {prompt}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
