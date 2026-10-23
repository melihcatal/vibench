# [LATER-STEP] stored_text_translate.py

import boto3
import json
import base64

from storage_client import get_managed_storage_client
from storage_models import ObjectMetadata


def translate_text(
    bucket_name: str, object_key: str, target_language: str = "es"
) -> dict:
    """Translate extracted text from a stored document using AWS Translate.

    Expects the caller to have already performed OCR or retrieved plain text.\n    Uses the text directly; for demo we read the object as a UTF‑8 string.
    Returns the translated text and confidence information.
    """
    client = get_managed_storage_client()
    # Retrieve object contents as text.
    obj = client.get_object(Bucket=bucket_name, Key=object_key)
    text = obj["Body"].read().decode("utf-8")

    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language
    )
    translated = response["TranslatedText"]
    return {
        "source_language": "en",
        "target_language": target_language,
        "translated_text": translated,
        "confidence": response.get("QualityScore"),  # optional
    }
