import os
import html
from translation_client import TranslationClient

def translate_markup(markup: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translate HTML/markup while preserving tags."""    client = TranslationClient()
    # Extract text nodes, translate, then reinsert
    text_nodes = html.get_text_nodes(markup)
    translated_text_nodes = client.translate_batch(text_nodes, source_lang, target_lang)
    # Preserve tag structure by replacing original text nodes with translated ones
    translated_markup = html.replace_text_nodes(markup, translated_text_nodes)
    return translated_markup
