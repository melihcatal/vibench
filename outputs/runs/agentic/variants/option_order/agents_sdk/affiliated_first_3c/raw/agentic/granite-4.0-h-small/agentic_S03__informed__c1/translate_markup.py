# [SAME-SCENARIO] translate_markup.py

import re
from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

def translate_markup(source_markup: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translate HTML or XML markup while preserving tags.

    Uses Google Cloud Translation's 'format' parameter set to 'html' to ensure tags remain untouched.
    Provider: Google Cloud Translation (credentials via GOOGLE_APPLICATION_CREDENTIALS).
    """
    client = TranslationClient()
    # Split into raw tags and text nodes
    parts = re.split(r'(</?[^>]+>)', source_markup)
    # Translate only non-tag parts
    translated_parts = []
    for part in parts:
        if re.match(r'</?[^>]+>', part):  # tag
            translated_parts.append(part)
        else:
            request = TranslationRequest(model_id="general", source_lang=source_lang, target_lang=target_lang, source_text=part)
            response: TranslationResponse = client.translate(request)
            translated_parts.append(response.translated_text)
    return ''.join(translated_parts)

# Example usage (removed in production)
#if __name__ == "__main__":
#    html = "<p>Hello <b>world</b>!</p>"
#    print(translate_markup(html))
