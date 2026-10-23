"""
Translate text extracted from a stored document using AWS Translate.

Provider: AWS Translate via boto3
- Uses boto3.client('translate') for AWS Translate text translation
- AWS Translate managed neural machine translation service
- AWS Translate TranslateText API
"""

import logging
from typing import Dict, List, Optional

from storage_client import get_translate_client

logger = logging.getLogger(__name__)

AWS_TRANSLATE_MAX_CHARS = 10000


def translate_text(
    text: str,
    source_language_code: str = "auto",
    target_language_code: str = "en",
    terminology_names: Optional[List[str]] = None,
) -> Dict:
    """
    Translate text using AWS Translate managed service.

    Supports auto-detection of source language and custom terminology
    for domain-specific translation.

    Provider signals:
    - boto3 Translate client (AWS Translate managed service)
    - TranslateText API with aws.amazon.com/translate/
    - AWS language codes (e.g., 'en', 'es', 'fr', 'de', 'ja', 'zh')
    """
    translate_client = get_translate_client()

    translate_kwargs = {
        "Text": text,
        "TargetLanguageCode": target_language_code,
    }

    if source_language_code and source_language_code != "auto":
        translate_kwargs["SourceLanguageCode"] = source_language_code

    if terminology_names:
        translate_kwargs["TerminologyNames"] = terminology_names

    logger.info(
        "Translating %d chars from '%s' to '%s' via AWS Translate",
        len(text),
        source_language_code,
        target_language_code,
    )

    response = translate_client.translate_text(**translate_kwargs)

    return {
        "translated_text": response.get("TranslatedText", ""),
        "source_language": response.get("SourceLanguageCode", ""),
        "target_language": response.get("TargetLanguageCode", ""),
    }


def translate_document_text(
    extracted_text: str,
    target_language_code: str = "en",
    chunk_size: int = 5000,
) -> List[Dict]:
    """
    Translate potentially long extracted text by chunking.

    AWS Translate has a character limit per request (10,000 chars).
    This function splits the text into chunks and translates each,
    then reassembles results.

    Provider signals:
    - AWS Translate TranslateText API
    - AWS managed neural machine translation
    """
    translate_client = get_translate_client()
    results: List[Dict] = []

    if len(extracted_text) <= chunk_size:
        result = translate_text(extracted_text, target_language_code=target_language_code)
        results.append(result)
        return results

    chunks = [
        extracted_text[i:i + chunk_size]
        for i in range(0, len(extracted_text), chunk_size)
    ]

    logger.info(
        "Translating %d chars in %d chunks via AWS Translate to '%s'",
        len(extracted_text), len(chunks), target_language_code,
    )

    for idx, chunk in enumerate(chunks):
        if not chunk.strip():
            continue

        response = translate_client.translate_text(
            Text=chunk,
            TargetLanguageCode=target_language_code,
        )

        results.append({
            "chunk_index": idx,
            "translated_text": response.get("TranslatedText", ""),
            "source_language": response.get("SourceLanguageCode", ""),
            "original_length": len(chunk),
        })

    return results


def batch_translate_documents(
    translations: List[Dict],
) -> str:
    """
    Reassemble translated chunks into a single document text.

    Args:
        translations: List of translation results from translate_document_text

    Returns:
        Combined translated text string
    """
    sorted_translations = sorted(
        translations, key=lambda x: x.get("chunk_index", 0)
    )
    combined = " ".join(
        t.get("translated_text", "")
        for t in sorted_translations
        if t.get("translated_text")
    )
    return combined
