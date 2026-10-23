from google.cloud import translate_v3 as translate
import os

from identity_client import GoogleCloudConfig
from identity_models import TranslateRequest, TranslateResponse


def welcome_translate(request: TranslateRequest) -> TranslateResponse:
    """
    Translates onboarding copy into the user's locale using Google Cloud Translation API.
    """
    if not GoogleCloudConfig.PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{GoogleCloudConfig.PROJECT_ID}"

    response = client.translate_text(
        request=translate.TranslateTextRequest(
            parent=parent,
            contents=[request.text],
            target_language_code=request.target_language_code,
            source_language_code=request.source_language_code,
        )
    )

    translated_text = ""
    detected_language_code = None

    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_language_code = response.translations[0].detected_language_code

    return TranslateResponse(
        translated_text=translated_text, detected_language_code=detected_language_code
    )
