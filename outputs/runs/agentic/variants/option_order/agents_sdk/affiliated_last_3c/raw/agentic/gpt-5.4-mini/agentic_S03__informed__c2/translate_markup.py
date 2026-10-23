from __future__ import annotations

from translation_client import get_client
from translation_models import extract_markup_text, rebuild_markup

PROVIDER = "azure-ai-translation-text"


def translate_markup(markup: str, source_language: str, target_language: str) -> str:
    client = get_client()
    text, parser = extract_markup_text(markup)
    if not text:
        return markup
    results = client.translate(body=[text], to_language=[target_language], from_parameter=source_language or None)
    translated = results[0].translations[0].text if results and results[0].translations else text
    return rebuild_markup(parser, translated)
