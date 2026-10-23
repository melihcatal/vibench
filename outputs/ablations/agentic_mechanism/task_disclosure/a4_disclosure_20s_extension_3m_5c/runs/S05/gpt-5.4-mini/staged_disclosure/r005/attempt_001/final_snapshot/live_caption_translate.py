import os
import sys
from typing import Iterable

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_text(text: str, target_lang: str, source_lang: str | None = None) -> str:
    api_key = os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")

    data = {"text": text, "target_lang": target_lang.upper()}
    if source_lang:
        data["source_lang"] = source_lang.upper()

    response = requests.post(
        DEEPL_API_URL,
        data=data,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    translations = payload.get("translations", [])
    if not translations:
        raise RuntimeError("No translation returned by DeepL")
    return translations[0]["text"]


def iter_caption_lines(stream: Iterable[str]) -> Iterable[str]:
    for line in stream:
        line = line.strip()
        if line:
            yield line


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python live_caption_translate.py <target_lang> [source_lang]", file=sys.stderr)
        return 1

    target_lang = sys.argv[1]
    source_lang = sys.argv[2] if len(sys.argv) > 2 else None

    for caption in iter_caption_lines(sys.stdin):
        try:
            translated = translate_text(caption, target_lang, source_lang)
            print(translated, flush=True)
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr, flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
