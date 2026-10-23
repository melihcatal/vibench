from translation_client import AmazonTranslateClient
from translation_models import normalize_language_code


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Translate a single text string using Amazon Translate."""
    client = AmazonTranslateClient()
    source_lang = normalize_language_code(source_lang)
    target_lang = normalize_language_code(target_lang)
    
    translated_text = client.translate_text(text, source_lang, target_lang)
    return translated_text if translated_text else ""