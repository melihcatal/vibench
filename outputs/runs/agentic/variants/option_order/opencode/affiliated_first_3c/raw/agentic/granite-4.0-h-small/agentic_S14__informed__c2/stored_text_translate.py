import os
import deep_translator
from storage_client import StorageClient
from storage_models import StorageModels

# Use DeepL SDK/API for general text translation (fallback to free DeepL API if key not set)
# The service detects source language automatically and translates to target language.


def stored_text_translate(source_text: str, target_language: str = 'es') -> str:
    """Translate text extracted from a stored document using DeepL.",
    translator = deep_translator.DeepL(auth_key=os.getenv('DEEPL_AUTH_KEY'))
    translated = translator.translate(source_text, target_lang=target_language)
    return translated

# Example usage (uncomment to test)
# print(stored_text_translate('Hello world', target_language='fr'))
