import os
from google.cloud import translate_v2 as translate
from identity_models import WelcomeTranslatePayload, WelcomeTranslateResponse

def welcome_translate(payload: WelcomeTranslatePayload) -> WelcomeTranslateResponse:
    # Google Cloud credentials are typically handled by GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or by running in a Google Cloud environment.
    translate_client = translate.Client()

    # Target language must be an ISO 639-1 code
    # Source language can be auto-detected if not provided
    result = translate_client.translate(
        payload.text,
        target_language=payload.target_language,
        source_language=payload.source_language
    )

    translated_text = result['translatedText']

    return WelcomeTranslateResponse(translated_text=translated_text)
