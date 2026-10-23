import os

import requests


def visual_safety_text(text: str):
    api_key = os.getenv("OPENAI_API_KEY")
    resp = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-5.4-mini",
            "input": f"Check this text for unsafe content: {text}",
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()
