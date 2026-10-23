from __future__ import annotations

from html.parser import HTMLParser
from typing import List, Tuple

from translation_client import PROVIDER_NAME, get_client
from translation_models import MarkupTranslationRequest, TranslationResponse


class _MarkupTranslator(HTMLParser):
    def __init__(self, client, source_language: str, target_language: str):
        super().__init__(convert_charrefs=False)
        self.client = client
        self.source_language = source_language
        self.target_language = target_language
        self.parts: List[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_text = ''.join(f' {k}="{v}"' for k, v in attrs)
        self.parts.append(f'<{tag}{attrs_text}>')

    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')

    def handle_data(self, data):
        if data.strip():
            translated = self.client.translate_text(data, source_lang=self.source_language, target_lang=self.target_language)
            self.parts.append(str(translated))
        else:
            self.parts.append(data)

    def translate(self, markup: str) -> str:
        self.feed(markup)
        self.close()
        return ''.join(self.parts)


def translate_markup(markup: str, source_language: str, target_language: str) -> TranslationResponse:
    client = get_client()
    request = MarkupTranslationRequest(markup=markup, source_language=source_language, target_language=target_language)
    translated = _MarkupTranslator(client, request.source_language, request.target_language).translate(request.markup)
    return TranslationResponse(text=translated, provider=PROVIDER_NAME, metadata={'model': 'deepl-api'})
