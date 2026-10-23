"""
Check live transcript text for unsafe content using Azure AI Content Safety API.

Analyzes streaming transcript text for hate speech, violence, sexual content,
and self-harm indicators using Azure AI Content Safety service.

Requires:
    pip install requests
"""

import os
from typing import Dict, Any, Optional, Iterator, List

import requests

from speech_models import TranscriptChunk, TranscriptStatus


AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/"
)
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"

SAFETY_CATEGORIES = [
    "Hate",
    "SelfHarm",
    "Sexual",
    "Violence",
]


def get_content_safety_config(
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, str]:
    """Get Azure AI Content Safety configuration.

    Args:
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Returns:
        Dictionary with endpoint and API key.
    """
    ep = endpoint or AZURE_CONTENT_SAFETY_ENDPOINT
    key = api_key or AZURE_CONTENT_SAFETY_KEY

    if not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_KEY environment variable is required"
        )

    return {
        "endpoint": ep.rstrip("/"),
        "api_key": key,
    }


def check_text_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Check text for unsafe content using Azure AI Content Safety.

    Sends text to Azure AI Content Safety API for analysis across
    Hate, SelfHarm, Sexual, and Violence categories.

    Args:
        text: Text to analyze for safety.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.
        categories: Specific categories to check. Defaults to all.

    Returns:
        Dictionary with safety analysis results including per-category scores.
    """
    if not text.strip():
        return {
            "text": text,
            "safe": True,
            "categories": {},
            "max_severity": 0,
        }

    config = get_content_safety_config(endpoint=endpoint, api_key=api_key)

    url = f"{config['endpoint']}/contentsafety/text:analyze"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}

    headers = {
        "Ocp-Apim-Subscription-Key": config["api_key"],
        "Content-Type": "application/json",
    }

    check_categories = categories or SAFETY_CATEGORIES
    body = {
        "text": text,
        "categories": check_categories,
    }

    response = requests.post(url, headers=headers, params=params, json=body)
    response.raise_for_status()

    result = response.json()

    categories_result = {}
    max_severity = 0
    for category_result in result.get("categoriesAnalysis", []):
        cat_name = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        categories_result[cat_name] = severity
        max_severity = max(max_severity, severity)

    is_safe = max_severity <= 2

    return {
        "text": text,
        "safe": is_safe,
        "categories": categories_result,
        "max_severity": max_severity,
        "blocklistsMatch": result.get("blocklistsMatch", []),
    }


def check_caption_safety(
    chunk: TranscriptChunk,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Check a transcript chunk for unsafe content.

    Args:
        chunk: TranscriptChunk to analyze.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Returns:
        Safety analysis result dictionary.
    """
    return check_text_safety(
        text=chunk.text,
        endpoint=endpoint,
        api_key=api_key,
    )


def check_live_captions_safety(
    caption_stream: Iterator[TranscriptChunk],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Iterator[Dict[str, Any]]:
    """Check a stream of live captions for unsafe content.

    Args:
        caption_stream: Iterator of TranscriptChunk objects to analyze.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Yields:
        Safety analysis result dictionaries for each chunk.
    """
    for chunk in caption_stream:
        if not chunk.text.strip():
            continue

        result = check_text_safety(
            text=chunk.text,
            endpoint=endpoint,
            api_key=api_key,
        )
        result["chunk"] = chunk
        yield result


def is_caption_safe(
    chunk: TranscriptChunk,
    threshold: int = 2,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> bool:
    """Check if a single caption chunk is safe based on severity threshold.

    Args:
        chunk: TranscriptChunk to check.
        threshold: Maximum allowed severity level (0-6, Azure scale).
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Returns:
        True if the caption is safe (all categories below threshold).
    """
    result = check_caption_safety(chunk, endpoint=endpoint, api_key=api_key)
    return result["max_severity"] <= threshold


def filter_unsafe_captions(
    caption_stream: Iterator[TranscriptChunk],
    threshold: int = 2,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Iterator[TranscriptChunk]:
    """Filter out unsafe captions from a stream.

    Args:
        caption_stream: Iterator of TranscriptChunk objects.
        threshold: Maximum allowed severity level.
        endpoint: Azure Content Safety endpoint URL.
        api_key: Azure Content Safety API key.

    Yields:
        Only safe TranscriptChunk objects.
    """
    for chunk in caption_stream:
        if is_caption_safe(chunk, threshold=threshold, endpoint=endpoint, api_key=api_key):
            yield chunk
        else:
            yield TranscriptChunk(
                text="[Content flagged for safety]",
                status=chunk.status,
                is_final=chunk.is_final,
                timestamp=chunk.timestamp,
            )


if __name__ == "__main__":
    test_chunks = [
        TranscriptChunk(text="Hello, how are you?", status=TranscriptStatus.FINAL, is_final=True),
        TranscriptChunk(text="This is a test of the safety filter.", status=TranscriptStatus.FINAL, is_final=True),
    ]

    for result in check_live_captions_safety(iter(test_chunks)):
        print(f"Text: {result['text'][:50]}... Safe: {result['safe']}")
