from typing import Optional
import os
from google.cloud import translate_v2 as translate
from .model_models import TranslationRequest, TranslationResponse


def localized_platform_output(
    text: str, target_language: str, source_language: Optional[str] = None
) -> TranslationResponse:
    """
    Translates platform model output for another locale using Google Cloud Translation.
    """
    client = translate.Client.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_language=result.get("detectedSourceLanguage"),
    )
