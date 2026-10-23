import os
from translation_client import get_translation_client


def translate_text(
    source_text: str, source_lang: str = "en", target_lang: str = "es"
) -> str:
    """Translate a single text string between languages.

    Uses Amazon Translate as the concrete provider.
    """
    client = get_translation_client()
    response = client.translate_text(
        Text=source_text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang,
    )
    return response.get("TranslatedText")
