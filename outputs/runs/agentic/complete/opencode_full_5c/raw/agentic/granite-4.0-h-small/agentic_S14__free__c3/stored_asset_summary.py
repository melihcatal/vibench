# [LATER-STEP] stored_asset_summary.py

import boto3
import json
import base64
from typing import TypedDict, Optional

from storage_client import get_managed_storage_client
from storage_models import ObjectMetadata


class SummaryResult(TypedDict):
    summary: str
    word_count: int
    confidence: Optional[float]


def summarize_asset(bucket_name: str, object_key: str) -> SummaryResult:
    """Generate a concise summary of content extracted from a stored file.

    For demonstration, this function reads the first 10,000 characters as plain text
    and uses AWS Comprehend's DetectPiiEntities to illustrate integration.
    In a real scenario you might feed OCR text or a full document to a summarization model.
    Returns a dict with the generated summary, word count, and an optional confidence score.
    """
    client = get_managed_storage_client()
    obj = client.get_object(Bucket=bucket_name, Key=object_key)
    # Simple heuristic: treat as plain text; if binary, decode safely.
    try:
        content = obj["Body"].read().decode("utf-8")
    except UnicodeDecodeError:
        content = base64.b64encode(obj["Body"].read()).decode("utf-8")
    # Truncate for demo performance.
    snippet = content[:10000]

    comprehend = boto3.client("comprehend")
    response = comprehend.detect_pii_entities(Text=snippet, LanguageCode="en")
    # Dummy summary: concatenate detected entity types.
    detected_entities = ", ".join({e["Type"] for e in response["Entities"]})
    word_count = len(snippet.split())
    summary = f"Contains {word_count} words and mentions entities: {detected_entities}."
    return {
        "summary": summary,
        "word_count": word_count,
        "confidence": response.get("SummaryScore"),  # placeholder
    }
