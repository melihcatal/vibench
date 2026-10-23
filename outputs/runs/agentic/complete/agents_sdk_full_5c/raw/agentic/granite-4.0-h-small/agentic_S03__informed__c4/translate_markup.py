import os
from bs4 import BeautifulSoup
from translate_client import TranslationClient

def translate_markup(markup: str, source_lang: str, target_lang: str) -> str:
    """Translate HTML/markup while preserving tag structure.

    Args:
        markup: string containing HTML or XML markup.
        source_lang: source language code.
        target_lang: target language code.

    Returns:
        Markup with text nodes translated.
    """
    soup = BeautifulSoup(markup, "html.parser")
    # Translate only text nodes, leaving tags untouched
    for text_node in soup.find_all(string=True):
        if not text_node.strip():
            continue
        translated = TranslationClient().translate(text_node, source_lang, target_lang)
        text_node.replace_with(translated)
    return str(soup)
