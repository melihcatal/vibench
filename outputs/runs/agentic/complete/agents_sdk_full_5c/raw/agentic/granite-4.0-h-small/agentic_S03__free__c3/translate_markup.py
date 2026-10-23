import os
import html
from translation_client import get_client
from translation_models import translate_request, normalize_response

def translate_markup(source_markup: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translate HTML/markup while preserving tags using Google Translate API.
    The implementation separates tags from text, translates only the text nodes, and reassembles the markup.
    """
    # Simple tag separator
    import re
    parts = re.split(r'(</?[^>]+>)', source_markup)
    translated_parts = []
    for part in parts:
        # Preserve tags as-is
        if re.match(r'<[^>]+>', part):
            translated_parts.append(part)
        else:
            # Translate text nodes
            client = get_client()
            request_data = translate_request(part, source_lang, target_lang)
            response = client.translate(request_data)
            translated_parts.append(normalize_response(response))
    return ''.join(translated_parts)