from translation_client import get_translation_client, get_project_id
from translation_models import TranslationRequest, TranslationResponse
from google.cloud import translate_v3beta1 as translate  # Provider-specific import


def translate_markup_text(request: TranslationRequest) -> TranslationResponse:
    # Ensure mime_type is set to "text/html" for markup translation
    if request.mime_type != "text/html":
        raise ValueError(
            "For markup translation, TranslationRequest.mime_type must be 'text/html'."
        )

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
        model=f"projects/{project_id}/locations/global/models/translate",  # Google Cloud Translation default model
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
