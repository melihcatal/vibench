import html
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import requests


TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"


@dataclass
class MarkupSegment:
    token: str
    text: str


class GoogleTranslateMarkupClient:
    def __init__(self, api_key: Optional[str] = None, session: Optional[requests.Session] = None):
        self.api_key = api_key or os.getenv("GOOGLE_TRANSLATE_API_KEY")
        self.session = session or requests.Session()

    def translate(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        if not self.api_key:
            raise ValueError("GOOGLE_TRANSLATE_API_KEY is required")
        params = {"key": self.api_key}
        data = {"q": text, "target": target_language, "format": "text"}
        if source_language:
            data["source"] = source_language
        response = self.session.post(TRANSLATE_URL, params=params, data=data, timeout=30)
        response.raise_for_status()
        payload = response.json()
        return payload["data"]["translations"][0]["translatedText"]


_TAG_RE = re.compile(r"(<[^>]+>|&[A-Za-z0-9#]+;)")


def _tokenize_markup(markup: str) -> Tuple[str, List[MarkupSegment]]:
    segments: List[MarkupSegment] = []
    parts = _TAG_RE.split(markup)
    tokens: List[str] = []
    text_index = 0
    for part in parts:
        if not part:
            continue
        if _TAG_RE.fullmatch(part):
            token = f"__MARKUP_{len(segments)}__"
            segments.append(MarkupSegment(token=token, text=part))
            tokens.append(token)
        else:
            tokens.append(part)
    return "".join(tokens), segments


def _restore_markup(text: str, segments: List[MarkupSegment]) -> str:
    restored = text
    for segment in segments:
        restored = restored.replace(segment.token, segment.text)
    return restored


def translate_markup(markup: str, target_language: str, source_language: Optional[str] = None, client: Optional[GoogleTranslateMarkupClient] = None) -> str:
    client = client or GoogleTranslateMarkupClient()
    tokenized, segments = _tokenize_markup(markup)
    translated = client.translate(tokenized, target_language=target_language, source_language=source_language)
    return _restore_markup(translated, segments)


def translate_markup_batch(markups: List[str], target_language: str, source_language: Optional[str] = None, client: Optional[GoogleTranslateMarkupClient] = None) -> List[str]:
    client = client or GoogleTranslateMarkupClient()
    return [translate_markup(markup, target_language=target_language, source_language=source_language, client=client) for markup in markups]
