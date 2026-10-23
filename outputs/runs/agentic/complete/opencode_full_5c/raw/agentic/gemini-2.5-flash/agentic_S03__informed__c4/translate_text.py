from translation_client import get_translation_client, get_project_id
from translation_models import TranslationRequest, TranslationResponse
from google.cloud import translate_v3beta1 as translate  # Provider-specific import


def translate_single_text(request: TranslationRequest) -> TranslationResponse:
    client = get_translation_client()
    project_id = get_project_id()
    if not project_id:
        raise ValueError(
            "Google Cloud Project ID not found. Ensure GOOGLE_CLOUD_PROJECT environment variable is set or authenticated with gcloud."
        )

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language_code,
        source_language_code=request.source_language_code,
        mime_type=request.mime_type,
    )

    translated_text = response.translations[0].translated_text
    detected_source_language_code = (
        response.translations[0].detected_language_code
        if response.translations[0].detected_language_code
        else None
    )

    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language_code=detected_source_language_code,
    )
