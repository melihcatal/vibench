from security_client import get_translate_client
from security_models import TranslationResult
import os

def translate_runbook_notes(
    text: str, 
    source_language_code: str, 
    target_language_code: str
) -> TranslationResult:
    """Translates secret-rotation runbook notes using AWS Translate.

    Args:
        text: The runbook notes text to translate.
        source_language_code: The language code of the input text (e.g., 'en', 'de').
        target_language_code: The language code to translate the text into (e.g., 'es', 'fr').

    Returns:
        A TranslationResult object containing the original and translated text, and language codes.
    """
    client = get_translate_client(region_name=os.environ.get('AWS_REGION', 'us-east-1'))
    try:
        response = client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )
        translated_text = response['TranslatedText']
        return TranslationResult(
            source_text=text,
            translated_text=translated_text,
            source_language=source_language_code,
            target_language=target_language_code
        )
    except Exception as e:
        raise RuntimeError(f"Error translating runbook notes with AWS Translate: {e}")
