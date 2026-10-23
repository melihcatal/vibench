import os
from storage_client import get_translate_client
from storage_models import TranslatedTextResponse

def translate_text(text_content: str, source_language_code: str, target_language_code: str) -> TranslatedTextResponse:
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=text_content,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return TranslatedTextResponse(
        translated_text=response['TranslatedText'],
        source_language_code=response['SourceLanguageCode'],
        target_language_code=response['TargetLanguageCode']
    )
