import os
import re
from google.cloud import translate_v2 as translate

TRANSLATE = translate.Client()

def translate_markup(markup: str, target_lang: str = "es") -> str:
    """Translate HTML or markup while preserving tags using Google Cloud Translation API.
    The function extracts text nodes, translates them, and re‑inserts them into the original markup.
    Args:
        markup: String containing HTML or any XML‑like markup.
        target_lang: Target language code.
    Returns:
        Markup with translated text content.
    """
    # Simple regex to split into tags and text nodes
    parts = re.split(r'(</?[^>]+>)', markup)
    translated_parts = []
    for part in parts:
        if part.startswith('<') and part.endswith('>'):
            # Preserve tag unchanged
            translated_parts.append(part)
        else:
            # Translate plain text
            translated = TRANSLATE.translate(part, target_language=target_lang)['translatedText']
            translated_parts.append(translated)
    return ''.join(translated_parts)