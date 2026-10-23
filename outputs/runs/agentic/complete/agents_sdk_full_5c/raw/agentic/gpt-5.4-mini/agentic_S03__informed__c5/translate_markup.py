from __future__ import annotations

from translation_client import get_azure_translator_client
from translation_models import MarkupPreservingHTMLParser


def translate_markup(source_language: str, target_language: str, markup: str) -> str:
    client = get_azure_translator_client()
    response = client.translate(body=[markup], from_parameter=source_language, to=[target_language], text_type="html")
    translated = response[0].translations[0].text if response else ""
    parser = MarkupPreservingHTMLParser()
    parser.feed(translated)
    return parser.get_markup()
