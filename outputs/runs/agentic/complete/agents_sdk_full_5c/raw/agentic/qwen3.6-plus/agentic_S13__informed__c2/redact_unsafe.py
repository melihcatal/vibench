"""
redact_unsafe.py - Flags or redacts unsafe spans from text.

Provider: Azure AI Content Safety
  - SDK: azure-ai-contentsafety
  - Env: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
  - Endpoint: .cognitiveservices.azure.com
  - Categories: Hate, SelfHarm, Sexual, Violence
"""

from __future__ import annotations

import re
from typing import Optional, List, Dict, Any

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

from safety_client import create_content_safety_client
from safety_models import (
    ModerationResponse,
    RedactionResult,
    normalize_azure_response,
    extract_unsafe_spans,
    AZURE_CATEGORIES,
)

CATEGORY_MAP = {
    "Hate": TextCategory.HATE,
    "SelfHarm": TextCategory.SELF_HARM,
    "Sexual": TextCategory.SEXUAL,
    "Violence": TextCategory.VIOLENCE,
}

DEFAULT_REDACTION_TOKEN = "[REDACTED]"


def redact_unsafe_text(
    text: str,
    categories: Optional[List[str]] = None,
    redaction_token: str = DEFAULT_REDACTION_TOKEN,
    client: Optional[ContentSafetyClient] = None,
) -> RedactionResult:
    """
    Analyze text and redact it if unsafe content is detected via Azure AI Content Safety.

    If any category exceeds severity 0, the entire text is replaced with the
    redaction token. For fine-grained span-level redaction, see
    redact_with_span_detection.

    Args:
        text: The input text to analyze and potentially redact.
        categories: Categories to check. Defaults to all Azure categories.
        redaction_token: Token to replace unsafe text with.
        client: Optional pre-configured ContentSafetyClient.

    Returns:
        RedactionResult with original text, redacted text, and flagged spans.
    """
    if not text or not text.strip():
        return RedactionResult(original_text=text, redacted_text=text)

    moderation_result = _moderate_for_redaction(text, categories, client)

    redaction = extract_unsafe_spans(
        text=text,
        categories=moderation_result.categories,
        redact_token=redaction_token,
    )

    return redaction


def redact_with_span_detection(
    text: str,
    categories: Optional[List[str]] = None,
    redaction_token: str = DEFAULT_REDACTION_TOKEN,
    client: Optional[ContentSafetyClient] = None,
    sentence_boundary: bool = True,
) -> RedactionResult:
    """
    Redact unsafe content at the sentence or paragraph level.

    Uses Azure AI Content Safety to detect overall text safety, then
    applies sentence-level granularity for redaction when unsafe content
    is detected.

    Args:
        text: The input text to analyze and redact.
        categories: Categories to check. Defaults to all Azure categories.
        redaction_token: Token to replace unsafe segments with.
        client: Optional pre-configured ContentSafetyClient.
        sentence_boundary: If True, split on sentences; otherwise use full text.

    Returns:
        RedactionResult with per-segment redaction details.
    """
    if not text or not text.strip():
        return RedactionResult(original_text=text, redacted_text=text)

    moderation_result = _moderate_for_redaction(text, categories, client)

    if moderation_result.overall_safe:
        return RedactionResult(
            original_text=text,
            redacted_text=text,
            flagged_spans=[],
            was_modified=False,
        )

    if sentence_boundary:
        segments = _split_sentences(text)
    else:
        segments = [text]

    flagged_spans = []
    redacted_segments = []
    current_pos = 0
    was_modified = False

    for segment in segments:
        segment_start = text.find(segment, current_pos)
        segment_end = segment_start + len(segment)

        try:
            seg_moderation = _moderate_for_redaction(segment, categories, client)
            is_segment_unsafe = not seg_moderation.overall_safe
        except Exception:
            is_segment_unsafe = False

        if is_segment_unsafe:
            redacted_segments.append(redaction_token)
            was_modified = True
            for cat in seg_moderation.categories:
                if cat.severity > 0:
                    flagged_spans.append({
                        "category": cat.category,
                        "severity": cat.severity,
                        "span": (segment_start, segment_end),
                        "redacted_value": redaction_token,
                    })
        else:
            redacted_segments.append(segment)

        current_pos = segment_end + 1

    redacted_text = " ".join(redacted_segments) if was_modified else text

    return RedactionResult(
        original_text=text,
        redacted_text=redacted_text,
        flagged_spans=flagged_spans,
        was_modified=was_modified,
    )


def flag_unsafe_text(
    text: str,
    categories: Optional[List[str]] = None,
    client: Optional[ContentSafetyClient] = None,
) -> Dict[str, Any]:
    """
    Flag unsafe text without modifying it. Returns detailed flag information.

    Args:
        text: The input text to analyze.
        categories: Categories to check.
        client: Optional pre-configured ContentSafetyClient.

    Returns:
        Dict with 'is_flagged', 'reasons', and 'moderation_response' keys.
    """
    moderation_result = _moderate_for_redaction(text, categories, client)

    reasons = []
    for cat in moderation_result.categories:
        if cat.severity > 0:
            reasons.append({
                "category": cat.category,
                "severity": cat.severity,
                "label": cat.label,
            })

    return {
        "is_flagged": not moderation_result.overall_safe,
        "reasons": reasons,
        "moderation_response": moderation_result,
    }


def _moderate_for_redaction(
    text: str,
    categories: Optional[List[str]],
    client: Optional[ContentSafetyClient],
) -> ModerationResponse:
    """Internal helper to moderate text for redaction workflows."""
    if client is None:
        client = create_content_safety_client()

    if categories is None:
        categories = AZURE_CATEGORIES

    text_categories = [CATEGORY_MAP[c] for c in categories if c in CATEGORY_MAP]

    options = AnalyzeTextOptions(
        text=text,
        categories=text_categories,
        output_type=0,
    )

    azure_response = client.analyze_text(options)
    return normalize_azure_response(text=text, azure_response=azure_response)


def _split_sentences(text: str) -> List[str]:
    """Split text into sentences using basic regex patterns."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]
