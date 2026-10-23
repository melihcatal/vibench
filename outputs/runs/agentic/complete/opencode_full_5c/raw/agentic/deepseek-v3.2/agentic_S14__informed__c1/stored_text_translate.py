import boto3
from botocore.exceptions import ClientError
from storage_client import get_translate_client
from storage_models import TranslationResult


def translate_extracted_text(
    text: str, target_language: str, source_language: str = "auto"
) -> TranslationResult:
    """
    Translate text extracted from a stored document using Amazon Translate.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Source language code or 'auto' for auto-detection (default: 'auto')

    Returns:
        TranslationResult object with translation details
    """
    translate_client = get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        return TranslationResult(
            original_text=text,
            translated_text=response["TranslatedText"],
            source_language=response["SourceLanguageCode"],
            target_language=target_language,
        )
    except ClientError as e:
        raise Exception(f"Translation failed: {e}")
