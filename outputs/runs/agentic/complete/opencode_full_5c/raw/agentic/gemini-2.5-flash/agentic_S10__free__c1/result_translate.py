import os
from google.cloud import translate_v3 as translate
from model_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request=translate.TranslateTextRequest(
            parent=parent,
            contents=[request.text],
            target_language_code=request.target_language,
            source_language_code=request.source_language
            if request.source_language
            else None,
        )
    )

    translated_text = ""
    metadata = {}
    if response.translations:
        translated_text = response.translations[0].translated_text
        metadata = {
            "detected_language_code": response.translations[0].detected_language_code
        }

    return TranslationResponse(translated_text=translated_text, metadata=metadata)
