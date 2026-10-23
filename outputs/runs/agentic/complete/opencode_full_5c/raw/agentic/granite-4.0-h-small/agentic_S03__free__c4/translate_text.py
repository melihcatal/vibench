# translate_text.py
from translation_client import get_client


def translate_text(source_text: str, source_lang: str, target_lang: str) -> str:
    """Translate a single text string between languages using the configured provider."""
    client = get_client()
    response = client.translate(
        text=source_text, source_lang=source_lang, target_lang=target_lang
    )
    return response.translated_text
