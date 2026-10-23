from typing import Optional, List
import os
from deep_translator import GoogleTranslator
from bs4 import BeautifulSoup
from translation_models import normalize_language_code


def translate_markup(
    markup: str,
    target_language: str,
    source_language: Optional[str] = None,
    ignore_tags: List[str] = [],
) -> str:
    normalized_target = normalize_language_code(target_language)
    normalized_source = (
        normalize_language_code(source_language) if source_language else None
    )

    soup = BeautifulSoup(markup, "html.parser")
    text_nodes = []

    for element in soup.find_all(string=True):
        if element.parent.name not in ignore_tags and element.strip():
            text_nodes.append((element, element.string))

    for element, text in text_nodes:
        translated_text = GoogleTranslator(
            source=normalized_source or "auto", target=normalized_target
        ).translate(text)
        element.string.replace_with(translated_text)

    return str(soup)
