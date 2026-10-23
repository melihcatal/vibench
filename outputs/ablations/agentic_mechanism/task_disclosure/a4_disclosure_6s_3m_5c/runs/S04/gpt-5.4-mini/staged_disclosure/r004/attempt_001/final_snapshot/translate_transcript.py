import os
import json
import argparse
from typing import Any, Dict, List
import requests

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

def translate_text(text: str, target_lang: str, source_lang: str | None = None) -> str:
    api_key = os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    data = {
        "text": text,
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        data["source_lang"] = source_lang.upper()
    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        data=data,
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["translations"][0]["text"]

def translate_completed_segments(segments: List[Dict[str, Any]], target_lang: str, source_lang: str | None = None) -> List[Dict[str, Any]]:
    translated = []
    for segment in segments:
        if segment.get("status") == "completed" and segment.get("text"):
            updated = dict(segment)
            updated["translated_text"] = translate_text(str(segment["text"]), target_lang, source_lang)
            translated.append(updated)
        else:
            translated.append(dict(segment))
    return translated

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--target-lang", required=True)
    parser.add_argument("--source-lang")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        segments = json.load(f)
    translated = translate_completed_segments(segments, args.target_lang, args.source_lang)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
