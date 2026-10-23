import os
from typing import Optional

import requests


GOOGLE_TRANSLATE_API_URL = "https://translation.googleapis.com/language/translate/v2"


def translate_stored_text(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_TRANSLATE_API_KEY is required")

    payload = {
        "q": text,
        "target": target_language,
        "format": "text",
        "key": api_key,
    }
    if source_language:
        payload["source"] = source_language

    response = requests.post(GOOGLE_TRANSLATE_API_URL, data=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    translations = data["data"]["translations"]
    if not translations:
        raise RuntimeError("No translation returned by Google Cloud Translation API")
    return translations[0]["translatedText"]


def main() -> None:
    stored_text = os.environ.get("STORED_DOCUMENT_TEXT")
    target_language = os.environ.get("TARGET_LANGUAGE", "en")
    source_language = os.environ.get("SOURCE_LANGUAGE")
    if not stored_text:
        raise RuntimeError("STORED_DOCUMENT_TEXT is required")
    print(translate_stored_text(stored_text, target_language, source_language))


if __name__ == "__main__":
    main()
