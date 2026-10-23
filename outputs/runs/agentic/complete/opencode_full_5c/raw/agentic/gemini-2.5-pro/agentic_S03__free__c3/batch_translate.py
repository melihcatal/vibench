from typing import List
from translation_client import google_translate_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    """
    Translates a list of strings.
    """
    results = google_translate_client.translate(
        request.source_texts,
        target_language=request.target_lang,
        source_language=request.source_lang,
    )

    translated_texts = [result["translatedText"] for result in results]
    detected_source_lang = ""
    if results:
        detected_source_lang = results[0].get("detectedSourceLanguage", "")

    return BatchTranslationResponse(
        translated_texts=translated_texts, detected_source_lang=detected_source_lang
    )
