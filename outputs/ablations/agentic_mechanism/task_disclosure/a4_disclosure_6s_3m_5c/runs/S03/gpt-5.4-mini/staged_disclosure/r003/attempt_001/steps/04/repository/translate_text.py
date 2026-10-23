import os
import sys
import requests


def translate_text(text, source_language, target_language):
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
                {"role": "system", "content": "You translate text accurately and only output the translation."},
                {"role": "user", "content": f"Translate from {source_language} to {target_language}: {text}"},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main():
    if len(sys.argv) < 4:
        raise SystemExit("Usage: translate_text.py <source_language> <target_language> <text>")
    source_language = sys.argv[1]
    target_language = sys.argv[2]
    text = " ".join(sys.argv[3:])
    print(translate_text(text, source_language, target_language))


if __name__ == "__main__":
    main()
