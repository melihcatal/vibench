from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse

def translate_text(text, source_lang, target_lang):
    client = get_translate_client()
    request = TranslationRequest(text, source_lang, target_lang)
    response = client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_lang,
        TargetLanguageCode=request.target_lang
    )
    return TranslationResponse(response['TranslatedText'])