from translation_client import get_translation_client, get_project_id
from translation_models import BatchTranslationRequest, BatchTranslationResponse
from google.cloud import translate_v3beta1

def batch_translate_texts(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = get_translation_client()
    project_id = get_project_id()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={'parent': parent,
                 'contents': request.texts,
                 'target_language_code': request.target_language_code,
                 'source_language_code': request.source_language_code,
                 'mime_type': 'text/plain'}
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    detected_source_language_codes = [translation.detected_language_code for translation in response.translations]

    return BatchTranslationResponse(translated_texts=translated_texts, detected_source_language_codes=detected_source_language_codes)
