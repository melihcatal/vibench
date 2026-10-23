import os
from google.cloud import translate_v3beta1 as translate
from document_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    """Translates text using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    parent = (
        f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}"  # Use a project ID from env
    )

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language,
            "source_language_code": request.source_language,
        }
    )

    translated_text = response.translations[0].translated_text
    return TranslationResponse(translated_text=translated_text)
