from google.cloud import translate_v2 as translate
from security_models import TranslateRequest, TranslateResponse

def translate_compliance_note(request: TranslateRequest) -> TranslateResponse:
    client = translate.Client()
    
    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language
    )
    
    return TranslateResponse(
        translated_text=result["translatedText"]
    )