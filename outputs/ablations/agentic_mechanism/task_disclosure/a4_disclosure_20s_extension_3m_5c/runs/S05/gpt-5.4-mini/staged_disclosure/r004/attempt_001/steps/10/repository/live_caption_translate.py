import json
import os
import sys
from typing import Iterable, Optional

from google.cloud import translate_v2 as translate


def translate_text(client: translate.Client, text: str, target_language: str, source_language: Optional[str] = None) -> str:
    if not text.strip():
        return text
    result = client.translate(text, target_language=target_language, source_language=source_language)
    translated = result.get("translatedText", "")
    return translated


def caption_lines(stream: Iterable[str], client: translate.Client, target_language: str) -> None:
    for line in stream:
        raw = line.strip()
        if not raw:
            continue
        try:
            payload = json.loads(raw)
            text = payload.get("text", raw)
            source_language = payload.get("source_language")
        except json.JSONDecodeError:
            text = raw
            source_language = None
        translated = translate_text(client, text, target_language, source_language)
        print(translated, flush=True)


def main() -> int:
    target_language = os.environ.get("TARGET_LANGUAGE", "es")
    client = translate.Client()
    caption_lines(sys.stdin, client, target_language)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
