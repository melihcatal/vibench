"""Translate text extracted from a stored document using AWS Translate.

Uses boto3 to call the AWS Translate service (model: translate.amazonaws.com,
using the base translation model) to translate extracted text.
Requires AWS credentials in environment variables:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

from storage_client import get_translate_client
from storage_models import TranslationResult


TRANSLATE_MODEL_ID = "aws-translate-base"


def stored_text_translate(text, target_language_code="en", source_language_code=None,
                          region=None, terminology_name=None):
    """Translate text extracted from a stored document using AWS Translate.

    Args:
        text: Source text to translate.
        target_language_code: ISO 639-1 target language code (e.g., "en", "es", "fr").
        source_language_code: ISO 639-1 source language code. If None, AWS auto-detects.
        region: Optional AWS region override.
        terminology_name: Optional custom terminology set name to apply.

    Returns:
        TranslationResult containing the translated text and metadata.

    Raises:
        botocore.exceptions.ClientError: If translation fails.
    """
    translate_client = get_translate_client(region=region)

    params = {
        "Text": text,
        "TargetLanguageCode": target_language_code,
    }
    if source_language_code:
        params["SourceLanguageCode"] = source_language_code

    response = translate_client.translate_text(**params)

    source_lang = response.get("SourceLanguageCode", source_language_code)
    target_lang = response.get("TargetLanguageCode", target_language_code)

    return TranslationResult(
        source_text=text,
        translated_text=response["TranslatedText"],
        source_language=source_lang,
        target_language=target_lang,
        model_id=TRANSLATE_MODEL_ID,
    )


def stored_text_translate_batch(texts, target_language_code="en",
                                source_language_code=None, region=None):
    """Translate multiple text strings using AWS Translate batch API.

    Args:
        texts: List of text strings to translate.
        target_language_code: ISO 639-1 target language code.
        source_language_code: Optional source language code.
        region: Optional AWS region override.

    Returns:
        List of TranslationResult objects, one per input text.
    """
    translate_client = get_translate_client(region=region)

    params = {
        "TargetLanguageCode": target_language_code,
    }
    if source_language_code:
        params["SourceLanguageCode"] = source_language_code

    results = []
    for text in texts:
        batch_params = dict(params, Text=text)
        response = translate_client.translate_text(**batch_params)
        results.append(TranslationResult(
            source_text=text,
            translated_text=response["TranslatedText"],
            source_language=response.get("SourceLanguageCode", source_language_code),
            target_language=response.get("TargetLanguageCode", target_language_code),
            model_id=TRANSLATE_MODEL_ID,
        ))

    return results
