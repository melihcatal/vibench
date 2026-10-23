from translation_client import get_translation_client
from translation_models import BatchTranslationRequest, TranslationResponse

def batch_translate(request: BatchTranslationRequest) -> list[TranslationResponse]:
    client = get_translation_client()
    parent = f"projects/{request.project_id}/locations/global"

    translated_responses = []
    for text_item in request.texts:
        response = client.translate_text(
            parent=parent,
            contents=[text_item],
            target_language_code=request.target_language,
            source_language_code=request.source_language,
            mime_type='text/plain'
        )
        translated_responses.append(TranslationResponse(translated_text=response.translations[0].translated_text))

    return translated_responses
