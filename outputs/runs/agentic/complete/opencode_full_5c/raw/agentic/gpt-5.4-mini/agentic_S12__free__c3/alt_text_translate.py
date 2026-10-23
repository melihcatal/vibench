import os

import requests


def alt_text_translate(text: str, language: str):
    api_key = os.getenv("OPENAI_API_KEY")
    resp = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-5.4-mini",
            "input": f"Translate this image description to {language}: {text}",
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()
