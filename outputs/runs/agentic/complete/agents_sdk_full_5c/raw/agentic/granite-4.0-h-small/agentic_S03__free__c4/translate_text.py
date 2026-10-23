import os
import json
from translation_client import TranslationClient

def translate_text(text: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translate a single text string between languages using a hypothetical external translation provider.
    Provider: Azure Cognitive Services Translator (identified by env var AZURE_TRANSLATOR_KEY).
    """
    client = TranslationClient()
    response = client.translate(text, source_lang, target_lang)
    # The provider returns a JSON list of translations; we extract the first.
    result = json.loads(response)[0]['translations'][0]['text']
    return result

if __name__ == '__main__':
    # Example usage (can be removed in production)
    sample = 'Hello, world!'
    print(f'Original: {sample}')
    print(f'Translated: {translate_text(sample)}')