from typing import Dict, Any
import os
from google.cloud import translate_v2 as translate
from identity_models import WelcomeTranslateRequest, WelcomeTranslateResponse

# Initialize Google Cloud Translation client with provider-specific credentials
translate_client = translate.Client()


def welcome_translate(request: WelcomeTranslateRequest) -> WelcomeTranslateResponse:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation.
    """
    try:
        result = translate_client.translate(
            request.text,
            target_language=request.target_locale,
            source_language=request.source_locale if request.source_locale else "auto",
        )
        return WelcomeTranslateResponse(
            success=True, translated_text=result["translatedText"]
        )
    except Exception as e:
        return WelcomeTranslateResponse(success=False, error=str(e))
