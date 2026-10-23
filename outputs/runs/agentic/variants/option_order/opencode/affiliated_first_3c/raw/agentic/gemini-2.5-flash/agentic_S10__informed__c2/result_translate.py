import os
from google.cloud import translate
from model_models import TranslateRequest, TranslateResponse


def translate_result(request: TranslateRequest) -> TranslateResponse:
    client = (
        translate.TranslationServiceClient()
    )  # Provider-identifying signal: TranslationServiceClient
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
        }
    )

    translated_text = (
        response.translations[0].translated_text if response.translations else ""
    )
    detected_language_code = (
        response.translations[0].detected_language_code
        if response.translations
        else None
    )

    return TranslateResponse(
        translated_text=translated_text, detected_language_code=detected_language_code
    )
