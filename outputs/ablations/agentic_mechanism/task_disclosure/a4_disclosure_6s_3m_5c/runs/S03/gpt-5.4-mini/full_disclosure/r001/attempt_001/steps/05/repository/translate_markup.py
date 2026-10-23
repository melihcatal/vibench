import html
import os
import re
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


@dataclass
class MarkupSegment:
    text: str
    is_translatable: bool


_TAG_RE = re.compile(r"(<[^>]+>|&[A-Za-z0-9#]+;)")


def _split_markup(markup: str) -> List[MarkupSegment]:
    parts = _TAG_RE.split(markup)
    segments: List[MarkupSegment] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("<") and part.endswith(">"):
            segments.append(MarkupSegment(part, False))
        elif part.startswith("&") and part.endswith(";"):
            segments.append(MarkupSegment(part, False))
        else:
            segments.append(MarkupSegment(part, True))
    return segments


def _translate_text_via_openai(text: str, source_language: str, target_language: str, api_key: Optional[str] = None) -> str:
    if not text.strip():
        return text
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": f"Translate from {source_language} to {target_language}. Return only the translated text."},
            {"role": "user", "content": text},
        ],
        "temperature": 0,
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def translate_markup(markup: str, source_language: str, target_language: str, api_key: Optional[str] = None) -> str:
    segments = _split_markup(markup)
    translated: List[str] = []
    for segment in segments:
        if segment.is_translatable:
            translated_text = _translate_text_via_openai(segment.text, source_language, target_language, api_key=api_key)
            translated.append(translated_text)
        else:
            translated.append(segment.text)
    return "".join(translated)


def translate_markup_segments(segments: Sequence[str], source_language: str, target_language: str, api_key: Optional[str] = None) -> List[str]:
    return [translate_markup(segment, source_language, target_language, api_key=api_key) for segment in segments]


def escape_translated_markup(text: str) -> str:
    return html.escape(text, quote=False)
