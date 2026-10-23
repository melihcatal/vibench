import os
from translation_client import TranslationClient
from translation_models import BatchTranslationRequest, BatchTranslationResponse
from google.cloud import translate  # provider-identifying signal


def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    client_wrapper = TranslationClient(project_id=project_id)
    client = client_wrapper.get_client()
    parent = client_wrapper.get_parent_path()

    response = client.translate_text(
        request.texts,
        request.target_language,
        parent,
        source_language_code=request.source_language,
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    detected_source_languages = [
        translation.detected_language_code for translation in response.translations
    ]

    return BatchTranslationResponse(
        translated_texts=translated_texts,
        detected_source_languages=detected_source_languages,
    )
