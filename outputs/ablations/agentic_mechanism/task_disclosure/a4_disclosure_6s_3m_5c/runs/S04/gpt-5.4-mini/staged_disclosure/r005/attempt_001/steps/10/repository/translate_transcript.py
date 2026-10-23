import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests


DEEPL_API_HOST = "https://api-free.deepl.com"


@dataclass
class TranscriptSegment:
    start: Any
    end: Any
    text: str
    translated_text: Optional[str] = None
    completed: bool = True


def _segment_text(segment: Dict[str, Any]) -> str:
    text = segment.get("text")
    if text is None:
        return ""
    return str(text)


def translate_text_deepl(text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
    api_key = os.environ.get("DEEPL_AUTH_KEY") or os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY or DEEPL_API_KEY must be set")

    payload = {"text": text, "target_lang": target_lang.upper()}
    if source_lang:
        payload["source_lang"] = source_lang.upper()

    response = requests.post(
        f"{DEEPL_API_HOST}/v2/translate",
        data=payload,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    translations = data.get("translations") or []
    if not translations:
        raise RuntimeError("DeepL returned no translations")
    return translations[0]["text"]


def translate_completed_segments(segments: Iterable[Dict[str, Any]], target_lang: str, source_lang: Optional[str] = None) -> List[Dict[str, Any]]:
    output: List[Dict[str, Any]] = []
    for segment in segments:
        completed = bool(segment.get("completed", True))
        item = dict(segment)
        if completed:
            text = _segment_text(segment)
            if text:
                item["translated_text"] = translate_text_deepl(text, target_lang, source_lang)
        output.append(item)
    return output


def main() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="-")
    parser.add_argument("--target-lang", required=True)
    parser.add_argument("--source-lang")
    args = parser.parse_args()

    if args.input == "-":
        payload = json.load(sys.stdin)
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            payload = json.load(f)

    segments = payload["segments"] if isinstance(payload, dict) and "segments" in payload else payload
    translated = translate_completed_segments(segments, args.target_lang, args.source_lang)
    json.dump(translated, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
