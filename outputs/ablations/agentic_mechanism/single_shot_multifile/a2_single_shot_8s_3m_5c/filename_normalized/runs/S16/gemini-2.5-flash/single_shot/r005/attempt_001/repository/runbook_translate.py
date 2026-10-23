import os
from security_client import get_translate_client

def translate_runbook_notes(text: str, source_language_code: str, target_language_code: str) -> str:
    client = get_translate_client()
    
    if not text:
        return ""

    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        return response['TranslatedText']
    except Exception:
        raise
