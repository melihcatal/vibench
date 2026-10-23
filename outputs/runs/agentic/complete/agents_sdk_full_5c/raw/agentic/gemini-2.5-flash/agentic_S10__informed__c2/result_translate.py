import os
from google.cloud import translate_v3 as translate
from model_models import TranslationRequest, TranslationResponse

def translate_result(request: TranslationRequest) -> TranslationResponse:
    """Translates generated model output using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    # Google Cloud Translation API identifies with 'google.cloud.translate_v3'
    # Requires GOOGLE_APPLICATION_CREDENTIALS or default credentials

    location = "global"
    parent = f"projects/{os.getenv("GOOGLE_CLOUD_PROJECT_ID")}/locations/{location}" if os.getenv("GOOGLE_CLOUD_PROJECT_ID") else f"projects/my-project-id/locations/{location}"

    response = client.translate_text(
        request=
            translate.TranslateTextRequest(
                parent=parent,
                contents=[request.text],
                target_language_code=request.target_language_code,
                source_language_code=request.source_language_code,
            )
    )

    translated_text = response.translations[0].translated_text if response.translations else ""
    detected_source_language = response.translations[0].detected_language_code if response.translations else None

    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language_code=detected_source_language
    )
