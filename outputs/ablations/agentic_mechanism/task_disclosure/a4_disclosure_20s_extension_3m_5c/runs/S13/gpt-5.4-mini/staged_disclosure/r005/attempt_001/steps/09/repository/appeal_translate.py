import os
import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_appeal_text(text: str, target_language: str = "English") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Translate appeal text accurately and preserve meaning, tone, and formatting."},
                {"role": "user", "content": f"Translate the following appeal text into {target_language}:\n\n{text}"},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: appeal_translate.py <text> [target_language]")

    appeal_text = sys.argv[1]
    target_language = sys.argv[2] if len(sys.argv) > 2 else "English"
    print(translate_appeal_text(appeal_text, target_language))
