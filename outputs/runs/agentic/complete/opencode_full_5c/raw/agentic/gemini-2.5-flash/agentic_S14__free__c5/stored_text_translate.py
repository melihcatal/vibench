import os
from google.cloud import translate_v2 as translate
from storage_models import TranslationRequest, TranslationResponse


def translate_stored_text(request: TranslationRequest) -> TranslationResponse:
    # Initialize Google Cloud Translation client
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should point to your service account key file
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            request.text,
            target_language=request.target_language,
            source_language=request.source_language,
        )
        translated_text = result["translatedText"]
        return TranslationResponse(
            success=True,
            translated_text=translated_text,
            message=f"Text translated successfully to {request.target_language}.",
        )
    except Exception as e:
        return TranslationResponse(
            success=False,
            translated_text=None,
            message=f"Failed to translate text: {str(e)}",
        )
