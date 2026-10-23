import os
from typing import Dict
import boto3
from security_client import get_translate_client
from security_models import TranslatedNote

def translate_compliance_note(text: str, source_language_code: str, target_language_code: str) -> TranslatedNote:
    """Translates an encryption or compliance note using AWS Translate."""
    translate_client = get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code, # e.g., 'en', 'es', 'fr'
            TargetLanguageCode=target_language_code  # e.g., 'de', 'ja', 'zh'
        )

        translated_text = response['TranslatedText']
        actual_source_language = response.get('SourceLanguageCode', source_language_code) # AWS might auto-detect if 'auto'

        return TranslatedNote(
            original_text=text,
            translated_text=translated_text,
            source_language=actual_source_language,
            target_language=target_language_code
        )

    except Exception as e:
        raise RuntimeError(f"Failed to translate compliance note with AWS Translate: {e}")