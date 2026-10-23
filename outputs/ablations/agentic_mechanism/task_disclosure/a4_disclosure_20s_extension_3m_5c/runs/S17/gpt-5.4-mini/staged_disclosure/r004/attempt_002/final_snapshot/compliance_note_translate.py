import os
from typing import Optional

import requests


GOOGLE_TRANSLATE_API_URL = "https://translation.googleapis.com/language/translate/v2"


def translate_compliance_note(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_TRANSLATE_API_KEY is required")

    payload = {"q": text, "target": target_language, "key": api_key, "format": "text"}
    if source_language:
        payload["source"] = source_language

    response = requests.post(GOOGLE_TRANSLATE_API_URL, data=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    translations = data["data"]["translations"]
    if not translations:
        raise RuntimeError("No translation returned by Google Cloud Translation API")
    return translations[0]["translatedText"]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("Usage: compliance_note_translate.py <target_language> <text> [source_language]")

    target = sys.argv[1]
    note = sys.argv[2]
    source = sys.argv[3] if len(sys.argv) > 3 else None
    print(translate_compliance_note(note, target, source))
