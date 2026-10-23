import os
from google.cloud import translate_v2 as translate
from embeddings_models import TranslationRequest, TranslationResponse


def translate_query(request: TranslationRequest) -> TranslationResponse:
    """
    Translates queries before multilingual embedding search using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set.
    """
    translate_client = translate.Client()

    if request.source_language == "auto":
        result = translate_client.translate(
            request.text, target_language=request.target_language
        )
    else:
        result = translate_client.translate(
            request.text,
            source_language=request.source_language,
            target_language=request.target_language,
        )

    return TranslationResponse(translated_text=result["translatedText"])
