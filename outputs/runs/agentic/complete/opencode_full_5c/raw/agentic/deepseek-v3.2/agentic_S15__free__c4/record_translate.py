import os
from database_client import get_translate_client
from database_models import TranslationRequest, TranslationResponse


def record_translate(request: TranslationRequest) -> TranslationResponse:
    """
    Translate user-facing document fields using Amazon Translate.
    """
    translate = get_translate_client()

    try:
        response = translate.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code,
        )

        return TranslationResponse(
            success=True,
            translated_text=response["TranslatedText"],
            source_language_code=response["SourceLanguageCode"],
            target_language_code=request.target_language_code,
            message="Text translated successfully using Amazon Translate",
        )
    except Exception as e:
        return TranslationResponse(
            success=False,
            translated_text="",
            source_language_code=request.source_language_code,
            target_language_code=request.target_language_code,
            error_message=str(e),
            message="Failed to translate text",
        )
