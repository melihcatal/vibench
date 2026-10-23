import json
import os
import sys
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _load_input() -> Dict[str, Any]:
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            return json.load(f)
    return json.load(sys.stdin)


def _translate_text(text: str, target_language: str, api_key: str) -> str:
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Translate the user's text accurately while preserving meaning, punctuation, and formatting.",
            },
            {
                "role": "user",
                "content": f"Translate the following text to {target_language}:\n\n{text}",
            },
        ],
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    data = _load_input()
    target_language = data.get("target_language", "English")
    segments = data.get("segments", [])
    if not isinstance(segments, list):
        raise TypeError("segments must be a list")

    translated_segments: List[Dict[str, Any]] = []
    for segment in segments:
        if not isinstance(segment, dict):
            continue
        if segment.get("status") != "completed":
            translated_segments.append(segment)
            continue
        text = str(segment.get("text", ""))
        if not text:
            translated_segments.append(segment)
            continue
        translated_segment = dict(segment)
        translated_segment["translated_text"] = _translate_text(text, target_language, api_key)
        translated_segments.append(translated_segment)

    output = dict(data)
    output["segments"] = translated_segments
    json.dump(output, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
