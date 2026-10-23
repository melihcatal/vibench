"""
stored_text_translate.py — Translate text extracted from a stored document.

Concrete provider: Amazon Translate via boto3 SDK.
Provider signals:
  - boto3 translate client creation ("translate")
  - AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY env vars
  - translate_text API call
"""

import os
from typing import Dict, List, Optional
from botocore.exceptions import ClientError

import boto3


def translate_extracted_text(
    source_text: str,
    source_language_code: str = "en",
    target_language_code: str = "es",
    terminology_name: Optional[str] = None,
) -> Dict:
    """
    Translate text extracted from a stored document using Amazon Translate.

    Parameters
    ----------
    source_text : str
        Text content to translate (e.g., OCR output).
    source_language_code : str
        ISO 639-1 language code of the source text (default "en").
    target_language_code : str
        ISO 639-1 language code for the translation (default "es").
    terminology_name : str, optional
        Name of a custom terminology resource in Amazon Translate.

    Returns
    -------
    dict
        Normalized translation result with translated text and metadata.

    Raises
    ------
    ClientError
        When the Translate API call fails.
    """
    translate_client = boto3.client("translate")

    translate_kwargs = {
        "Text": source_text,
        "SourceLanguageCode": source_language_code,
        "TargetLanguageCode": target_language_code,
    }

    if terminology_name:
        translate_kwargs["TerminologyNames"] = [terminology_name]

    response = translate_client.translate_text(**translate_kwargs)

    return {
        "translated_text": response.get("TranslatedText", ""),
        "source_language": response.get("SourceLanguageCode", source_language_code),
        "target_language": response.get("TargetLanguageCode", target_language_code),
        "service": "Amazon Translate",
        "original_length": len(source_text),
        "translated_length": len(response.get("TranslatedText", "")),
    }


def translate_document_segments(
    segments: List[str],
    source_language_code: str = "en",
    target_language_code: str = "es",
    batch_size: int = 5,
) -> List[Dict]:
    """
    Translate a list of text segments (e.g., lines from OCR) in batches.

    Amazon Translate supports batch translate via TranslateText per segment.
    For true batch operations, TranslateDocument could be used for S3-stored files.

    Parameters
    ----------
    segments : list[str]
        List of text segments to translate.
    source_language_code : str
        Source language code.
    target_language_code : str
        Target language code.
    batch_size : int
        Number of segments per API call.

    Returns
    -------
    list[dict]
        Per-segment translation results.
    """
    translate_client = boto3.client("translate")
    results = []

    for i in range(0, len(segments), batch_size):
        batch = segments[i:i + batch_size]
        for segment in batch:
            if not segment.strip():
                results.append({
                    "original": segment,
                    "translated": "",
                    "source_language": source_language_code,
                    "target_language": target_language_code,
                })
                continue

            try:
                response = translate_client.translate_text(
                    Text=segment,
                    SourceLanguageCode=source_language_code,
                    TargetLanguageCode=target_language_code,
                )
                results.append({
                    "original": segment,
                    "translated": response.get("TranslatedText", ""),
                    "source_language": response.get("SourceLanguageCode", source_language_code),
                    "target_language": response.get("TargetLanguageCode", target_language_code),
                })
            except ClientError as e:
                results.append({
                    "original": segment,
                    "translated": None,
                    "error": str(e),
                })

    return results
