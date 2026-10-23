from typing import List
from translation_client import get_translation_client
from translation_models import TranslationResponse


def batch_translate(
    texts: List[str], source_language: str, target_language: str
) -> List[TranslationResponse]:
    """
    Translates a list of strings using Google Cloud Translation.
    """
    client = get_translation_client()

    results = client.translate(
        texts, target_language=target_language, source_language=source_language
    )

    responses = [
        TranslationResponse(
            translated_text=result["translatedText"],
            detected_source_language=result.get("detectedSourceLanguage"),
        )
        for result in results
    ]

    return responses
