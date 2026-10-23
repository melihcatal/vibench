from google.cloud import translate_v2 as translate
from typing import Optional


def translate_text_from_stored_document(
    text: str, target_language: str = "en", source_language: Optional[str] = None
) -> str:
    """
    Translate text extracted from a stored document using Google Cloud Translation API.
    """
    client = translate.Client()
    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )
    return result["translatedText"]