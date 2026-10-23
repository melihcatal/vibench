import os
import re
from html.parser import HTMLParser
from typing import List, Optional, Tuple

import requests


_OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
_OPENAI_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini")


class _MarkupSegmenter(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.parts: List[Tuple[str, str]] = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(
            f' {name}' if value is None else f' {name}="{value}"' for name, value in attrs
        )
        self.parts.append(("tag", f"<{tag}{attrs_text}>"))

    def handle_endtag(self, tag):
        self.parts.append(("tag", f"</{tag}>"))

    def handle_startendtag(self, tag, attrs):
        attrs_text = "".join(
            f' {name}' if value is None else f' {name}="{value}"' for name, value in attrs
        )
        self.parts.append(("tag", f"<{tag}{attrs_text} />"))

    def handle_data(self, data):
        self.parts.append(("text", data))

    def handle_comment(self, data):
        self.parts.append(("tag", f"<!--{data}-->"))

    def handle_entityref(self, name):
        self.parts.append(("tag", f"&{name};"))

    def handle_charref(self, name):
        self.parts.append(("tag", f"&#{name};"))


def _translate_text(text: str, source_language: str, target_language: str, api_key: Optional[str]) -> str:
    if not text.strip():
        return text
    if api_key is None:
        raise ValueError("OPENAI_API_KEY is required")
    response = requests.post(
        _OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": _OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You translate text while preserving meaning, punctuation, spacing, and formatting hints. Return only the translated text.",
                },
                {
                    "role": "user",
                    "content": f"Translate from {source_language} to {target_language}: {text}",
                },
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def translate_markup(markup: str, source_language: str, target_language: str, api_key: Optional[str] = None) -> str:
    parser = _MarkupSegmenter()
    parser.feed(markup)
    translated_parts: List[str] = []
    for kind, value in parser.parts:
        if kind == "text":
            translated_parts.append(_translate_text(value, source_language, target_language, api_key))
        else:
            translated_parts.append(value)
    return "".join(translated_parts)
