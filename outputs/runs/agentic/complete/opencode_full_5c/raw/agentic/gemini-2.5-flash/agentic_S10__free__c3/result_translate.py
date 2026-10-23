import os
from google.cloud import translate_v3 as translate
from model_models import TranslationRequest, TranslationResponse

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def translate_text(request: TranslationRequest) -> TranslationResponse:
    """Translates generated model output using Google Cloud Translation API."""
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()  # Using google.cloud.translate_v3

    parent = f"projects/{PROJECT_ID}/locations/global"

    response = client.translate_text(
        request=dict(
            parent=parent,
            contents=[request.text],
            mime_type="text/plain",  # Mime types: "text/plain", "text/html"
            source_language_code=request.source_language_code,
            target_language_code=request.target_language_code,
        )
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    return TranslationResponse(translated_text=translated_text)
