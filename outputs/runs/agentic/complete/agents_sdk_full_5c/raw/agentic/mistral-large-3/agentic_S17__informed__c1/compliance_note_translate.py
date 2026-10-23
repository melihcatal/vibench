from security_client import get_translate_client
from security_models import TranslationRequest, TranslationResponse

def translate_compliance_note(text: str, source_lang: str, target_lang: str) -> TranslationResponse:
    client = get_translate_client()
    request = TranslationRequest(text=text, source_lang=source_lang, target_lang=target_lang)

    # Amazon Translate integration
    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_lang,
        TargetLanguageCode=request.target_lang
    )
    
    return TranslationResponse(
        translated_text=response['TranslatedText']
    )