import boto3
from document_client import get_translate_client

def translate_text(text: str, source_language_code: str, target_language_code: str) -> str:
    """
    Translates extracted OCR text using AWS Translate.
    Source and target language codes should be valid ISO 639-1 codes (e.g., 'en', 'es', 'fr').
    """
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )
    return response['TranslatedText']
