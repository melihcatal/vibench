from google.cloud import translate_v3 as translate
from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate_texts(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = get_translation_client()
    parent = f"projects/{request.project_id}/locations/{request.location}"
    
    response = client.translate_text(
        parent=parent,
        contents=request.texts,
        target_language_code=request.target_language,
        source_language_code=request.source_language,
    )
    
    translated_texts = [translation.translated_text for translation in response.translations]
    return BatchTranslationResponse(translated_texts=translated_texts)
