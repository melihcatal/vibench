import os
from model_client import get_translate_client

def translate_text_output(text: str, source_language_code: str = "en", target_language_code: str = "es") -> str:
    translate_client = get_translate_client()
    
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    
    return response["TranslatedText"]
