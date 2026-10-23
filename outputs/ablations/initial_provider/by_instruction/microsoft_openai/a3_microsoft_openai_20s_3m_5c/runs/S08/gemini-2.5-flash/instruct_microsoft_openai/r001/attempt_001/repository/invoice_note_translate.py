from document_client import get_google_translate_client # Concrete provider: Google Cloud Translation API
from typing import Optional

def translate_text(text: str, target_language: str = 'en', source_language: Optional[str] = None) -> str:
    client = get_google_translate_client()

    # The target language should be an ISO 639-1 code
    # The source language can be auto-detected if not provided
    if source_language:
        result = client.translate(text, target_language=target_language, source_language=source_language)
    else:
        result = client.translate(text, target_language=target_language)

    return result['translatedText']
