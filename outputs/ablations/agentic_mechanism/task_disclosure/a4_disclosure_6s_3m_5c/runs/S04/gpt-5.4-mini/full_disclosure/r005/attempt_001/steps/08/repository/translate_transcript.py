import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _auth_headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _segment_text(segment: Dict[str, Any]) -> str:
    text = segment.get("text")
    if text is None:
        text = segment.get("transcript")
    if text is None:
        text = segment.get("content")
    return "" if text is None else str(text)


def translate_transcript(segments: List[Dict[str, Any]], target_language: str) -> List[Dict[str, Any]]:
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Translate transcript segments faithfully. Preserve names, numbers, and timestamps. Return only the translated text.",
            },
            {
                "role": "user",
                "content": {
                    "target_language": target_language,
                    "segments": [
                        {"index": i, "text": _segment_text(segment)} for i, segment in enumerate(segments)
                    ],
                },
            },
        ],
        "temperature": 0,
    }
    response = requests.post(OPENAI_API_URL, headers=_auth_headers(), json=payload, timeout=120)
    response.raise_for_status()
    translated = response.json()["choices"][0]["message"]["content"]
    if isinstance(translated, str):
        translated_segments = [line for line in translated.splitlines() if line.strip()]
    else:
        translated_segments = [str(translated)]
    result: List[Dict[str, Any]] = []
    for i, segment in enumerate(segments):
        item = dict(segment)
        item["translated_text"] = translated_segments[i] if i < len(translated_segments) else ""
        item["target_language"] = target_language
        result.append(item)
    return result


__all__ = ["translate_transcript"]
