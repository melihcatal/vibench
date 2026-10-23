import json
import os
import requests


def main():
    api_key = os.environ["OPENAI_API_KEY"]
    text = os.getenv("LOG_TEXT", "")
    target_language = os.getenv("TARGET_LANGUAGE", "es")
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Translate support-visible log messages while preserving technical identifiers."},
                {"role": "user", "content": f"Translate to {target_language}: {text}"},
            ],
            "temperature": 0.2,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print(json.dumps(main(), default=str))