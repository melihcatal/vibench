import os
from safety_client import get_google_translate_client

def translate_appeal_text(text: str, target_language: str = "en", source_language: str = None) -> str:
    client = get_google_translate_client()

    translation_result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )
    
    if translation_result and translation_result[0] and 'translatedText' in translation_result[0]:
        return translation_result[0]['translatedText']
    else:
        return text
