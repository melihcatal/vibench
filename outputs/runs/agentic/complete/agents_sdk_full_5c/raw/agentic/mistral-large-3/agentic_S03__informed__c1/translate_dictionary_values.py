from typing import Dict, Any
from translation_client import AmazonTranslateClient
from translation_models import normalize_language_code


def translate_dictionary_values(data: Dict[str, Any], source_lang: str, target_lang: str) -> Dict[str, Any]:
    """Translate dictionary values while preserving keys using Amazon Translate."""
    client = AmazonTranslateClient()
    source_lang = normalize_language_code(source_lang)
    target_lang = normalize_language_code(target_lang)
    
    def translate_value(value: Any) -> Any:
        if isinstance(value, str):
            translated_text = client.translate_text(value, source_lang, target_lang)
            return translated_text if translated_text else value
        elif isinstance(value, list):
            return [translate_value(item) for item in value]
        elif isinstance(value, dict):
            return translate_dictionary_values(value, source_lang, target_lang)
        else:
            return value
    
    return {key: translate_value(value) for key, value in data.items()}