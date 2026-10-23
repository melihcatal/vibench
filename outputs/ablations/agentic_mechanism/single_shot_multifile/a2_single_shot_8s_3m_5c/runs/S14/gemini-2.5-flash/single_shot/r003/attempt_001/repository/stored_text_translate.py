import os
from storage_client import get_translate_client

def translate_text(text: str, source_language_code: str, target_language_code: str) -> str:
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response.get('TranslatedText', '')
