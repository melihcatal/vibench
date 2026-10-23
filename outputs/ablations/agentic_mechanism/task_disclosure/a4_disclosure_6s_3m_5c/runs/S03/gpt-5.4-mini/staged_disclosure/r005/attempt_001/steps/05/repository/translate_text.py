import os
import sys
import requests


def translate_text(text: str, source_language: str, target_language: str) -> str:
    api_key = os.getenv("DEEPL_AUTH_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")

    response = requests.post(
        "https://api-free.deepl.com/v2/translate",
        data={
            "auth_key": api_key,
            "text": text,
            "source_lang": source_language,
            "target_lang": target_language,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations", [])
    if not translations:
        raise RuntimeError("No translation returned by DeepL")
    return translations[0]["text"]


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("Usage: translate_text.py <text> <source_language> <target_language>")
    print(translate_text(sys.argv[1], sys.argv[2], sys.argv[3]))


if __name__ == "__main__":
    main()
