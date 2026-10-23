"""
Summarize visual analysis results using OpenAI GPT-4 API.
Provider: OpenAI API (openai)
Endpoint: api.openai.com
Model: gpt-4o-mini
"""

from __future__ import annotations

import json
import os
from typing import Optional

import openai


def summarize_visual_analysis(
    labels: list[dict],
    description: str,
    detected_text: Optional[str] = None,
    safety_result: Optional[dict] = None,
    model: str = "gpt-4o-mini",
) -> dict:
    """
    Summarize visual analysis results into a concise, human-readable summary.

    Uses OpenAI GPT-4 API to synthesize label detection, image description,
    OCR text, and safety analysis into a coherent summary.

    Args:
        labels: List of detected labels with name and confidence.
        description: Generated image description text.
        detected_text: Optional OCR-extracted text from the image.
        safety_result: Optional safety analysis result dictionary.
        model: OpenAI model identifier (default: gpt-4o-mini).

    Returns:
        Dictionary with summary text, key findings, and safety assessment.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY", "")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    safety_text = ""
    if safety_result:
        safe_status = safety_result.get("overall_status", "UNKNOWN")
        flagged = safety_result.get("flagged_categories", [])
        safety_text = f"Safety Status: {safe_status}."
        if flagged:
            flags = ", ".join(f"{f['category']} ({f['likelihood']})" for f in flagged)
            safety_text += f" Flagged: {flags}."

    text_content = ""
    if detected_text:
        text_content = f"\nExtracted text: {detected_text[:500]}"

    label_list = ", ".join(
        f"{l.get('label', l.get('name', 'unknown'))} ({l.get('confidence', l.get('score', 0)):.0%})"
        for l in labels[:10]
    )

    prompt = (
        f"Provide a concise visual analysis summary based on the following data:\n\n"
        f"Image Description: {description}\n"
        f"Detected Labels: {label_list}\n"
        f"{safety_text}\n"
        f"{text_content}\n\n"
        f"Return a JSON object with these fields:\n"
        f"- summary: A 2-3 sentence plain text summary of the image content\n"
        f"- key_elements: List of the most important visual elements (max 5)\n"
        f"- content_type: Classification (e.g., photograph, illustration, screenshot, document, other)\n"
        f"- audience_appropriate: Boolean indicating if suitable for general audiences\n"
        f"- confidence: Float between 0 and 1 indicating analysis confidence\n"
    )

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a visual analysis assistant. Summarize image analysis results concisely."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    content = response.choices[0].message.content.strip()

    try:
        summary_data = json.loads(content)
    except json.JSONDecodeError:
        summary_data = {
            "summary": content,
            "key_elements": [],
            "content_type": "unknown",
            "audience_appropriate": True,
            "confidence": 0.5,
        }

    return {
        "provider": "openai",
        "model": model,
        "summary": summary_data.get("summary", ""),
        "key_elements": summary_data.get("key_elements", []),
        "content_type": summary_data.get("content_type", "unknown"),
        "audience_appropriate": summary_data.get("audience_appropriate", True),
        "confidence": summary_data.get("confidence", 0.0),
    }


def summarize_for_report(
    analysis_results: dict,
    include_raw_data: bool = False,
    model: str = "gpt-4o-mini",
) -> dict:
    """
    Create a report-ready summary from complete visual analysis results.

    Args:
        analysis_results: Dictionary containing labels, description, text, and safety data.
        include_raw_data: Whether to include raw analysis data in output.
        model: OpenAI model identifier.

    Returns:
        Report-ready summary dictionary.
    """
    labels = analysis_results.get("labels", [])
    description = analysis_results.get("description", "")
    detected_text = analysis_results.get("detected_text")
    safety = analysis_results.get("safety")

    summary = summarize_visual_analysis(
        labels=labels,
        description=description,
        detected_text=detected_text,
        safety_result=safety,
        model=model,
    )

    report = {
        "summary": summary,
        "source": analysis_results.get("source", "unknown"),
    }

    if include_raw_data:
        report["raw_data"] = analysis_results

    return report


if __name__ == "__main__":
    import sys

    sample = {
        "labels": [
            {"label": "sky", "confidence": 0.98},
            {"label": "mountain", "confidence": 0.95},
            {"label": "nature", "confidence": 0.92},
        ],
        "description": "A scenic mountain landscape with blue sky",
        "detected_text": "National Park",
        "safety": {"overall_status": "SAFE", "flagged_categories": []},
    }

    result = summarize_visual_analysis(**sample)
    print(json.dumps(result, indent=2))
