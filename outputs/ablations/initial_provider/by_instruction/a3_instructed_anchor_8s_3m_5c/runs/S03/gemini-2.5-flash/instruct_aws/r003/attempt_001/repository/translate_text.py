from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse

def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = get_translate_client()
    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code
    )
    return TranslationResponse(
        translated_text=response['TranslatedText'],
        source_language_code=response['SourceLanguageCode'],
        target_language_code=response['TargetLanguageCode']
    )
