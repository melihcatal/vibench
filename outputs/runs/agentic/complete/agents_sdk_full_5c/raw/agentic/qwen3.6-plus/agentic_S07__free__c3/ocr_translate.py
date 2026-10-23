"""
Translate extracted OCR text using AWS Translate.

Provider: AWS Translate
Model/Feature: AWS Translate TranslateText API with specific language codes
"""

import os
from typing import List, Optional

import boto3
from botocore.config import Config

from document_models import TranslationRequest, TranslationResponse


# Provider-identifying: AWS Translate endpoint and model
AWS_TRANSLATE_ENDPOINT = os.environ.get(
    "AWS_TRANSLATE_ENDPOINT", "https://translate.us-east-1.amazonaws.com"
)
AWS_TRANSLATE_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# AWS Translate model identifiers for specific language pairs
TEXTRACT_DEFAULT_MODEL = "nmt"  # Neural Machine Translation


def create_translate_client(
    region_name: Optional[str] = None,
    max_retries: int = 3,
    timeout: int = 30,
) -> boto3.client:
    """
    Create a boto3 Translate client.

    Args:
        region_name: AWS region
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds

    Returns:
        Configured boto3 Translate client
    """
    config = Config(
        retries={"max_attempts": max_retries},
        connect_timeout=timeout,
        read_timeout=timeout,
    )

    session_kwargs = {"region_name": region_name or AWS_TRANSLATE_REGION}
    if AWS_ACCESS_KEY and AWS_SECRET_KEY:
        session_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY
        session_kwargs["aws_secret_access_key"] = AWS_SECRET_KEY

    return boto3.client("translate", config=config, **session_kwargs)


def translate_ocr_text(
    text: str,
    source_language: str = "en",
    target_language: str = "es",
) -> TranslationResponse:
    """
    Translate extracted OCR text using AWS Translate.

    Uses the AWS Translate TranslateText API to translate text between
    supported language codes (e.g., 'en' to 'es', 'en' to 'fr').

    Args:
        text: Extracted OCR text to translate
        source_language: Source language code (e.g., 'en')
        target_language: Target language code (e.g., 'es')

    Returns:
        TranslationResponse with translated text and metadata
    """
    client = create_translate_client()

    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )

    translated_text = response.get("TranslatedText", "")

    # ApplyTerminologyResponse may contain confidence data
    applied_terminology = response.get("AppliedTerminologies", [])

    return TranslationResponse(
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        confidence=_calculate_confidence(applied_terminology, text),
    )


def translate_ocr_response(
    full_text: str,
    source_language: str = "en",
    target_language: str = "es",
    max_chunk_size: int = 5000,
) -> TranslationResponse:
    """
    Translate full OCR response text, chunking if necessary.

    AWS Translate has a character limit per request; this handles chunking
    automatically for large documents.

    Args:
        full_text: Full extracted OCR text
        source_language: Source language code
        target_language: Target language code
        max_chunk_size: Maximum characters per API call

    Returns:
        TranslationResponse with fully translated text
    """
    if len(full_text) <= max_chunk_size:
        return translate_ocr_text(full_text, source_language, target_language)

    # Split on sentence boundaries for clean chunking
    chunks = _split_text_into_chunks(full_text, max_chunk_size)
    translated_chunks = []

    for chunk in chunks:
        if not chunk.strip():
            continue
        result = translate_ocr_text(chunk.strip(), source_language, target_language)
        translated_chunks.append(result.translated_text)

    return TranslationResponse(
        translated_text=" ".join(translated_chunks),
        source_language=source_language,
        target_language=target_language,
        confidence=0.0,
    )


def translate_text_batch(
    texts: List[str],
    source_language: str = "en",
    target_language: str = "es",
) -> List[TranslationResponse]:
    """
    Translate a batch of text segments using AWS Translate BatchTranslateText.

    Args:
        texts: List of text strings to translate
        source_language: Source language code
        target_language: Target language code

    Returns:
        List of TranslationResponse objects
    """
    # For batch, we call translate_text individually but could use
    # AWS Translate BatchTranslateText with S3 for large volumes
    results = []
    for text in texts:
        if text.strip():
            result = translate_ocr_text(text, source_language, target_language)
            results.append(result)
    return results


def detect_source_language(text: str) -> str:
    """
    Detect the source language of text using AWS Translate.

    Args:
        text: Text to analyze

    Returns:
        Detected language code
    """
    client = create_translate_client()

    response = client.detect_dominant_language(Text=text)
    languages = response.get("Languages", [])

    if languages:
        return languages[0].get("LanguageCode", "en")
    return "en"


def _calculate_confidence(applied_terminologies: list, original_text: str) -> float:
    """
    Calculate a rough confidence score for translation.

    Args:
        applied_terminologies: Applied terminology list from response
        original_text: Original text length indicator

    Returns:
        Confidence value between 0 and 1
    """
    # AWS Translate doesn't return a direct confidence score,
    # so we estimate based on terminology application
    if applied_terminologies:
        return 0.95
    return 0.9


def _split_text_into_chunks(text: str, max_size: int) -> List[str]:
    """
    Split text into chunks for API limits.

    Args:
        text: Text to split
        max_size: Maximum chunk size in characters

    Returns:
        List of text chunks
    """
    chunks = []
    current = ""

    # Split on sentence boundaries
    sentences = text.replace("\n", ". ").split(". ")

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(current) + len(sentence) + 2 > max_size:
            if current:
                chunks.append(current.strip())
                current = sentence
            else:
                # Single sentence exceeds limit; force split
                for i in range(0, len(sentence), max_size):
                    chunks.append(sentence[i:i + max_size])
        else:
            if current:
                current += ". " + sentence
            else:
                current = sentence

    if current.strip():
        chunks.append(current.strip())

    return chunks


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ocr_translate.py <text_file> [target_language]")
        sys.exit(1)

    text_file = sys.argv[1]
    target_lang = sys.argv[2] if len(sys.argv) > 2 else "es"

    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()

    result = translate_ocr_response(text, target_language=target_lang)
    print(f"Translated ({result.source_language} -> {result.target_language}):")
    print(result.translated_text[:500])
