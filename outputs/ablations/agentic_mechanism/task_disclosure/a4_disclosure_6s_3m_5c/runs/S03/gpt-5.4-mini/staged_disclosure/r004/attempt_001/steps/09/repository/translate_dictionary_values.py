import json
import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _translate_text(text: str, target_language: str) -> str:
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
                {"role": "system", "content": "Translate the user's text while preserving meaning."},
                {"role": "user", "content": f"Translate this text to {target_language}: {text}"},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def translate_dictionary_values(data: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = _translate_text(value, target_language)
        elif isinstance(value, dict):
            translated[key] = translate_dictionary_values(value, target_language)
        else:
            translated[key] = value
    return translated


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("target_language")
    parser.add_argument("input_file")
    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = translate_dictionary_values(data, args.target_language)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
