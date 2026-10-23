import os
import re
from translation_client import TranslationClient

def translate_markup(markup: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translate text inside HTML/markup while preserving tags and attributes.
    Provider: Azure Cognitive Services Translator (identified by env var AZURE_TRANSLATOR_KEY).
    """
    # Simple regex to separate tags from text nodes (non-greedy)
    parts = re.split(r'(</?[^>]+>)', markup)
    translated_parts = []
    for part in parts:
        # If part looks like a tag, keep it unchanged
        if re.match(r'<[^>]+>', part):
            translated_parts.append(part)
        else:
            # Translate plain text
            translated_parts.append(translate_text(part, source_lang, target_lang))
    return ''.join(translated_parts)

if __name__ == '__main__':
    sample_html = '<p>Hello <strong>world</strong>!</p>'
    print('Original:', sample_html)
    print('Translated:', translate_markup(sample_html))