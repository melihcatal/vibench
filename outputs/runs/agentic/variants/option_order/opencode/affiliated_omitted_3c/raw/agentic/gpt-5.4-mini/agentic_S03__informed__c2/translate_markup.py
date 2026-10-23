from __future__ import annotations

from html.parser import HTMLParser
from typing import List

from translation_client import TranslationClient
from translation_models import TranslationRequest

_client = TranslationClient()


class _MarkupTranslator(HTMLParser):
    def __init__(self, source_language: str, target_language: str) -> None:
        super().__init__()
        self.source_language = source_language
        self.target_language = target_language
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_text = ''.join(f' {k}="{v}"' for k, v in attrs)
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if data.strip():
            translated = _client.translate(TranslationRequest(source_language=self.source_language, target_language=self.target_language, text=data)).translated_text
            self.parts.append(translated)
        else:
            self.parts.append(data)


def translate_markup(markup: str, source_language: str, target_language: str) -> str:
    parser = _MarkupTranslator(source_language, target_language)
    parser.feed(markup)
    return ''.join(parser.parts)
