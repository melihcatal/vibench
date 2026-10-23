"""Translate text extracted from a stored document using AWS Translate."""

from typing import Optional

from storage_client import S3ClientFactory
from storage_models import TranslationRequest, TranslationResult


def translate_stored_text(
    text: str,
    target_language: str = "en",
    source_language: str = "auto",
) -> TranslationResult:
    """
    Translate text extracted from a stored document using AWS Translate.

    Calls the AWS Translate TranslateText API endpoint
    (translate.us-east-1.amazonaws.com) to translate text between
    supported language pairs. AWS Translate supports over 75 languages
    and automatically detects the source language when set to 'auto'.

    Args:
        text: The source text to translate (up to 10,000 bytes per request).
        target_language: Target ISO 639-1 language code (e.g., 'en', 'fr', 'de').
        source_language: Source ISO 639-1 language code, or 'auto' for detection.

    Returns:
        TranslationResult with translated text and detected source language.

    Raises:
        botocore.exceptions.ClientError: If the language pair is unsupported
            or the text exceeds the service limit.
        ValueError: If target_language is not a valid language code.
    """
    factory = S3ClientFactory()
    translate_client = factory.get_translate_client()

    translate_params = {
        "Text": text,
        "TargetLanguageCode": target_language,
    }

    if source_language and source_language.lower() != "auto":
        translate_params["SourceLanguageCode"] = source_language

    response = translate_client.translate_text(**translate_params)

    translated_text = response.get("TranslatedText", "")
    detected_source = response.get("SourceLanguageCode", source_language)

    return TranslationResult(
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language,
        character_count=len(text),
    )


def translate_stored_text_batch(
    texts: list,
    target_language: str = "en",
    source_language: str = "auto",
) -> list:
    """
    Translate multiple text segments using AWS Translate.

    Processes a list of text segments sequentially via the TranslateText API.
    AWS Translate does not support batch translation in a single API call
    for the synchronous TranslateText endpoint.

    Args:
        texts: List of text strings to translate.
        target_language: Target language code.
        source_language: Source language code or 'auto'.

    Returns:
        List of TranslationResult, one per input text.
    """
    results = []
    for text in texts:
        if not text or not text.strip():
            results.append(TranslationResult(
                translated_text="",
                source_language=source_language,
                target_language=target_language,
                character_count=0,
            ))
            continue

        result = translate_stored_text(
            text=text,
            target_language=target_language,
            source_language=source_language,
        )
        results.append(result)

    return results
