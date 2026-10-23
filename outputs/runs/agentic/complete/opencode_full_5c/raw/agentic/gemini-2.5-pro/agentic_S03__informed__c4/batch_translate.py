from typing import List
from translation_client import get_translation_client
from translation_models import TranslationResponse, BatchTranslationResponse


def batch_translate(
    texts: List[str], target_language: str, source_language: str | None = None
) -> BatchTranslationResponse:
    """
    Translates a list of strings.
    """
    client = get_translation_client()
    results = client.translate(
        texts,
        target_language=target_language,
        source_language=source_language if source_language else "",
    )

    responses = [
        TranslationResponse(
            translated_text=res["translatedText"],
            detected_source_language=res.get("detectedSourceLanguage"),
        )
        for res in results
    ]
    return BatchTranslationResponse(translations=responses)
