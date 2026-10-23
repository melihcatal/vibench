from translation_client import get_translation_client, get_project_id
from translation_models import BatchTranslationRequest, BatchTranslationResponse
from google.cloud import translate_v3beta1 as translate  # Provider-specific import


def batch_translate_texts(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = get_translation_client()
    project_id = get_project_id()
    if not project_id:
        raise ValueError(
            "Google Cloud Project ID not found. Ensure GOOGLE_CLOUD_PROJECT environment variable is set or authenticated with gcloud."
        )

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=request.texts,
        target_language_code=request.target_language_code,
        source_language_code=request.source_language_code,
        mime_type=request.mime_type,
    )

    translated_texts = [t.translated_text for t in response.translations]
    detected_source_language_codes = [
        t.detected_language_code if t.detected_language_code else None
        for t in response.translations
    ]

    return BatchTranslationResponse(
        translations=translated_texts,
        detected_source_language_codes=detected_source_language_codes,
    )
