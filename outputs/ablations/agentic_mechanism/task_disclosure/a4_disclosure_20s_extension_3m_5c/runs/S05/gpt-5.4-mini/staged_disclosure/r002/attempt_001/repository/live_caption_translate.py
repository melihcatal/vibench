import os
import sys
from typing import Optional

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_caption(text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_API_KEY is required")

    payload = {"text": text, "target_lang": target_lang.upper()}
    if source_lang:
        payload["source_lang"] = source_lang.upper()

    response = requests.post(
        DEEPL_API_URL,
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["translations"][0]["text"]


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: live_caption_translate.py TARGET_LANG CAPTION_TEXT [SOURCE_LANG]", file=sys.stderr)
        return 2

    target_lang = sys.argv[1]
    caption_text = sys.argv[2]
    source_lang = sys.argv[3] if len(sys.argv) > 3 else None

    translated = translate_caption(caption_text, target_lang, source_lang)
    print(translated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
