import os
from typing import Dict, Any
from translation_client import TranslationClient

def translate_dictionary_values(dictionary: Dict[str, str], source_lang: str = 'en', target_lang: str = 'es') -> Dict[str, str]:
    """Translate all string values in a dictionary while preserving keys."""    client = TranslationClient()
    translated_values = client.translate_batch(list(dictionary.values()), source_lang, target_lang)
    return {k: v for k, v in zip(dictionary.keys(), translated_values)}
