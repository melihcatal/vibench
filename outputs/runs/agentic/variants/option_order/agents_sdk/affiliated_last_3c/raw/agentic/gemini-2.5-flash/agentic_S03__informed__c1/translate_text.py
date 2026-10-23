from google.cloud import translate_v3 as translate
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_single_text(request: TranslationRequest) -> TranslationResponse:
    client = get_translation_client()
    parent = f"projects/{request.project_id}/locations/{request.location}"
    
    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language,
        source_language_code=request.source_language,
    )
    
    translated_text = response.translations[0].translated_text
    return TranslationResponse(translated_text=translated_text)
