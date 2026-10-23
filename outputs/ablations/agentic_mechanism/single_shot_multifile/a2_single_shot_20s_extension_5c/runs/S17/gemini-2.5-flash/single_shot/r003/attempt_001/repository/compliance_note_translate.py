import os
from security_client import get_translate_client
from security_models import TranslationRequest, TranslationResponse
from google.cloud import translate_v3 as translate

def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    translate_client = get_translate_client()
    
    parent = f"projects/{request.project_id}/locations/global"
    
    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language,
            "source_language_code": request.source_language
        }
    )
    
    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text
        
    return TranslationResponse(translated_text=translated_text)
