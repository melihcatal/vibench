import os
import re
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_markup(markup_text: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translates HTML or XML markup while preserving tags.
    The function extracts text nodes, translates them, and reassembles the markup.
    """
    client = get_translation_client()
    # Simple regex to split into tag and text parts
    parts = re.split(r'(</?[^>]+>)', markup_text)
    translated_parts = []
    for part in parts:
        if re.match(r'^</?[^>]+>$', part):
            # Preserve tag as-is
            translated_parts.append(part)
        else:
            # Translate text node
            req = TranslationRequest(text=part, source_lang=source_lang, target_lang=target_lang)
            resp: TranslationResponse = client.translate(req)
            translated_parts.append(resp.translated_text)
    return ''.join(translated_parts)
