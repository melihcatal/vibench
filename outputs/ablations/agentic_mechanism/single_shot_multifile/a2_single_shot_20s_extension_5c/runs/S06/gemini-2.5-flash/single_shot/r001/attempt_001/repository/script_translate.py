import os
from speech_client import get_translate_client
from speech_models import TranslationRequest

def translate_script(request: TranslationRequest) -> str:
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code
    )
    return response['TranslatedText']
