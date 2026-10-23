import os
import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_runbook_notes(text: str, target_language: str = "en") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "Translate secret-rotation runbook notes accurately and preserve operational details."},
            {"role": "user", "content": f"Translate the following runbook notes to {target_language}:\n\n{text}"},
        ],
        "temperature": 0,
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    import sys

    source = sys.stdin.read()
    if not source.strip():
        raise SystemExit(0)
    translated = translate_runbook_notes(source)
    sys.stdout.write(translated)


if __name__ == "__main__":
    main()
