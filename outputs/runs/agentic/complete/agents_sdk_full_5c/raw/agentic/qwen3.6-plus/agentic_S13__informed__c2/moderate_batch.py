"""
moderate_batch.py - Moderates a batch of user messages and returns per-message decisions.

Provider: Azure AI Content Safety
  - SDK: azure-ai-contentsafety
  - Env: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
  - Endpoint: .cognitiveservices.azure.com
"""

from __future__ import annotations

import logging
from typing import Optional, List

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from safety_client import create_content_safety_client
from safety_models import (
    ModerationResponse,
    BatchModerationResponse,
    normalize_azure_response,
    AZURE_CATEGORIES,
)

logger = logging.getLogger(__name__)

CATEGORY_MAP = {
    "Hate": TextCategory.HATE,
    "SelfHarm": TextCategory.SELF_HARM,
    "Sexual": TextCategory.SEXUAL,
    "Violence": TextCategory.VIOLENCE,
}


def moderate_batch(
    texts: List[str],
    categories: Optional[List[str]] = None,
    client: Optional[ContentSafetyClient] = None,
    max_concurrent: int = 5,
) -> BatchModerationResponse:
    """
    Moderate a batch of text messages using Azure AI Content Safety.

    Each message is analyzed independently and results are collected
    into a BatchModerationResponse.

    Args:
        texts: List of text messages to moderate.
        categories: Optional list of categories to check.
        client: Optional pre-configured ContentSafetyClient.
        max_concurrent: Maximum number of concurrent API calls.

    Returns:
        BatchModerationResponse with per-message moderation results.

    Raises:
        ValueError: If texts list is empty.
    """
    if not texts:
        raise ValueError("Texts list must not be empty.")

    if client is None:
        client = create_content_safety_client()

    if categories is None:
        categories = AZURE_CATEGORIES

    text_categories = [CATEGORY_MAP[c] for c in categories if c in CATEGORY_MAP]

    results: List[ModerationResponse] = []

    for idx, text in enumerate(texts):
        if not text or not text.strip():
            logger.warning("Skipping empty text at index %d", idx)
            results.append(ModerationResponse(text="", overall_safe=True))
            continue

        try:
            options = AnalyzeTextOptions(
                text=text,
                categories=text_categories,
                output_type=0,
            )
            azure_response = client.analyze_text(options)
            result = normalize_azure_response(text=text, azure_response=azure_response)
        except Exception as exc:
            logger.error("Error moderating text at index %d: %s", idx, exc)
            result = ModerationResponse(
                text=text,
                overall_safe=False,
                raw_response={"error": str(exc)},
            )

        results.append(result)

    return BatchModerationResponse(results=results)


def moderate_batch_with_filtering(
    texts: List[str],
    categories: Optional[List[str]] = None,
    client: Optional[ContentSafetyClient] = None,
    allow_only_safe: bool = True,
) -> dict:
    """
    Moderate a batch and optionally filter to only safe messages.

    Args:
        texts: List of text messages to moderate.
        categories: Optional list of categories to check.
        client: Optional pre-configured ContentSafetyClient.
        allow_only_safe: If True, separate safe and unsafe messages.

    Returns:
        Dict with 'safe_texts', 'unsafe_texts', and 'batch_response' keys.
    """
    batch_response = moderate_batch(texts, categories=categories, client=client)

    safe_texts = []
    unsafe_texts = []

    for result in batch_response.results:
        if result.overall_safe:
            safe_texts.append(result.text)
        else:
            unsafe_texts.append(result.text)

    return {
        "safe_texts": safe_texts,
        "unsafe_texts": unsafe_texts,
        "batch_response": batch_response,
    }


def get_batch_summary(batch_response: BatchModerationResponse) -> dict:
    """
    Generate a summary of batch moderation results.

    Args:
        batch_response: The batch moderation response to summarize.

    Returns:
        Summary dict with counts and category breakdowns.
    """
    category_counts = {}
    for result in batch_response.results:
        for cat in result.categories:
            if cat.severity > 0:
                category_counts[cat.category] = category_counts.get(cat.category, 0) + 1

    return {
        "total_items": batch_response.total_items,
        "safe_count": batch_response.total_items - batch_response.unsafe_count,
        "unsafe_count": batch_response.unsafe_count,
        "unsafe_rate": (
            batch_response.unsafe_count / batch_response.total_items
            if batch_response.total_items > 0
            else 0.0
        ),
        "category_breakdown": category_counts,
    }
