from google.cloud import translate_v2 as translate
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse
import os

def translate_stored_text(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    """Translates text extracted from a stored document using Google Cloud Translation."""
    client = translate.Client()

    result = client.translate(
        request.text,
        target_language=request.target_language_code,
        source_language=request.source_language_code
    )

    return StoredTextTranslateResponse(
        original_text=request.text,
        translated_text=result['translatedText'],
        source_language_code=result['detectedSourceLanguage'] if 'detectedSourceLanguage' in result else request.source_language_code,
        target_language_code=request.target_language_code
    )
