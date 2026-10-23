import os
from translation_client import create_translator_client
from translation_models import TranslationResponse

def batch_translate(texts: list[str], target_lang: str = "es") -> list[str]:
    """Translate a list of strings preserving order.",
    client = create_translator_client()
    responses = client.translate(
        texts=texts,
        to_language=target_lang
    )
    return [TranslationResponse(r).get_translated_text() for r in responses]
