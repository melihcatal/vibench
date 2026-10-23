import os
import requests


def translate_appeal_text(text: str, target_language: str = "en") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

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
                    "content": "Translate appeal text for review. Return only the translated text.",
                },
                {
                    "role": "user",
                    "content": f"Translate the following appeal text into {target_language}: {text}",
                },
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
