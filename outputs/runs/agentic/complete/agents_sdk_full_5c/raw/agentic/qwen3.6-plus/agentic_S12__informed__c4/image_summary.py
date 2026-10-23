"""
image_summary.py - Summarize visual analysis results
using Anthropic Messages API (anthropic SDK).

Provider: Anthropic Messages API
SDK: anthropic
Auth: ANTHROPIC_API_KEY
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional

import anthropic

from vision_models import (
    ImageDescription,
    LabelDetectionResponse,
    SafetyScoreResponse,
    TextDetectionResponse,
)


ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def summarize_visual_analysis(
    label_response: Optional[LabelDetectionResponse] = None,
    description_response: Optional[ImageDescription] = None,
    text_response: Optional[TextDetectionResponse] = None,
    safety_response: Optional[SafetyScoreResponse] = None,
    api_key: Optional[str] = None,
    model: str = ANTHROPIC_MODEL,
    max_tokens: int = 1024,
) -> str:
    """Generate a concise summary of visual analysis results via Anthropic Claude.

    Args:
        label_response: Results from label detection.
        description_response: Results from image description.
        text_response: Results from text/OCR detection.
        safety_response: Results from safety scoring.
        api_key: Anthropic API key (falls back to ANTHROPIC_API_KEY env var).
        model: Anthropic model identifier.
        max_tokens: Maximum response tokens.

    Returns:
        A natural-language summary string of the combined analysis.
    """
    client = anthropic.Anthropic(api_key=api_key)

    parts: List[str] = []
    parts.append(
        "You are a visual analysis summarizer. Given the following structured "
        "image analysis results, produce a concise, well-organized summary "
        "(3-6 short paragraphs or bullet points) that captures the key "
        "visual elements, any detected text, and the safety assessment.\n"
    )

    if label_response and label_response.labels:
        label_items = ", ".join(
            f"{l.label} ({l.confidence:.2f})" for l in label_response.labels[:8]
        )
        parts.append(f"Detected Labels: {label_items}")

    if description_response:
        parts.append(f"Image Description: {description_response.description}")
        parts.append(f"Confidence: {description_response.confidence:.2f}")

    if text_response and text_response.full_text:
        parts.append(f"Detected Text: {text_response.full_text[:500]}")

    if safety_response:
        safe_status = "SAFE" if safety_response.is_safe else "FLAGGED"
        parts.append(f"Safety Status: {safe_status}")
        if safety_response.flagged_categories:
            parts.append(
                f"Flagged: {', '.join(safety_response.flagged_categories)}"
            )
        rating_summaries = []
        for r in safety_response.ratings:
            score = r.likelihood_score if r.likelihood_score is not None else 0
            rating_summaries.append(f"{r.category}: {r.likelihood} ({score:.2f})")
        parts.append(f"Safety Ratings: {'; '.join(rating_summaries)}")

    user_message = "\n\n".join(parts)

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=0.3,
        system=(
            "You summarize visual analysis reports from Google Cloud Vision. "
            "Be concise and objective. Structure the output clearly."
        ),
        messages=[
            {"role": "user", "content": user_message},
        ],
    )

    summary_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            summary_text += block.text

    return summary_text


def format_summary_report(summary: str) -> str:
    """Format the summary for display."""
    lines = [
        "=== Visual Analysis Summary (Anthropic Claude) ===",
        "",
        summary,
        "",
        "---",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    # Minimal demo: build dummy responses and summarize
    sample_labels = LabelDetectionResponse(
        labels=[],
        raw_response={"provider": "google-cloud-vision"},
    )
    sample_desc = ImageDescription(
        description="A sunny landscape with mountains and a lake.",
        confidence=0.92,
        topics=["mountain", "lake", "landscape", "nature"],
    )
    sample_text = TextDetectionResponse(
        texts=[],
        full_text="Welcome to Yosemite National Park",
    )
    sample_safety = SafetyScoreResponse(
        ratings=[],
        is_safe=True,
        flagged_categories=[],
    )

    result = summarize_visual_analysis(
        label_response=sample_labels,
        description_response=sample_desc,
        text_response=sample_text,
        safety_response=sample_safety,
    )
    print(format_summary_report(result))
