import os
import sys
from typing import Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_text(text: str, source_lang: Optional[str], target_lang: str) -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")

    data = {"text": text, "target_lang": target_lang.upper()}
    if source_lang:
        data["source_lang"] = source_lang.upper()

    response = requests.post(
        DEEPL_API_URL,
        data=data,
        headers={"Authorization": f"DeepL-Auth-Key {auth_key}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["translations"][0]["text"]


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("Usage: translate_text.py TARGET_LANG TEXT [SOURCE_LANG]")

    target_lang = sys.argv[1]
    text = sys.argv[2]
    source_lang = sys.argv[3] if len(sys.argv) > 3 else None
    print(translate_text(text, source_lang, target_lang))


if __name__ == "__main__":
    main()
