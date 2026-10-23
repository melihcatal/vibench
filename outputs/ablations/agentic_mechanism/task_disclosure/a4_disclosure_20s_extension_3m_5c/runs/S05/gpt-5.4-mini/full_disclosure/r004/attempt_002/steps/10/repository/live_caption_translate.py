import os
import requests


def translate_live_caption(text: str, target_language: str) -> str:
    api_key = os.environ["OPENAI_API_KEY"]
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-5.4-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a precise translation engine for live captions. Return only the translated text.",
                },
                {
                    "role": "user",
                    "content": f"Translate the following live caption into {target_language}: {text}",
                },
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
