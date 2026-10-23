from security_client import deepl_client
from security_models import TranslationRequest, TranslationResponse

def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    """
    Translates a compliance note to a target language using DeepL API.
    """
    try:
        client = deepl_client
        response_data = client.translate(
            text=request.text,
            target_lang=request.target_language
        )
        
        translation = response_data['translations'][0]
        
        return TranslationResponse(
            translated_text=translation['text'],
            detected_source_language=translation['detected_source_language'],
            success=True
        )
    except Exception as e:
        return TranslationResponse(
            translated_text="",
            detected_source_language="",
            success=False,
            error=str(e)
        )
