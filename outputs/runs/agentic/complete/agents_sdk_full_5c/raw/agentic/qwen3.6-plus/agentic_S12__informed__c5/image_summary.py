"""
Summarize visual analysis results using Google Gemini API.

Provider: Google Gemini API
SDK: google-genai
Auth: GOOGLE_API_KEY
Model: gemini-2.0-flash
"""

import os
import json
from typing import Optional, List, Dict, Any

from google import genai
from google.genai import types

from detect_image_labels import LabelDetectionResponse
from describe_image import ImageDescriptionResponse
from detect_image_text import TextDetectionResponse
from score_image_safety import SafetyModerationResponse


def summarize_visual_analysis(
    labels_response: Optional[LabelDetectionResponse] = None,
    description_response: Optional[ImageDescriptionResponse] = None,
    text_response: Optional[TextDetectionResponse] = None,
    safety_response: Optional[SafetyModerationResponse] = None,
    model: str = "gemini-2.0-flash",
    api_key: Optional[str] = None,
    summary_style: str = "concise",
) -> str:
    """
    Summarize visual analysis results using Google Gemini API (gemini-2.0-flash).

    Takes the outputs from image label detection, description, text detection,
    and safety scoring, then generates a coherent natural-language summary.

    Args:
        labels_response: Output from detect_image_labels.
        description_response: Output from describe_image.
        text_response: Output from detect_image_text.
        safety_response: Output from score_image_safety.
        model: Gemini model identifier (default: gemini-2.0-flash).
        api_key: Google API key override.
        summary_style: Style of summary ('concise', 'detailed', 'structured').

    Returns:
        A string containing the summarized visual analysis.
    """
    key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set")

    client = genai.Client(api_key=key)

    analysis_parts = _build_analysis_context(
        labels_response,
        description_response,
        text_response,
        safety_response,
    )

    style_instructions = {
        "concise": "Provide a concise 2-3 sentence summary.",
        "detailed": "Provide a detailed paragraph-by-paragraph summary.",
        "structured": "Provide a structured summary with labeled sections for objects, description, text, and safety.",
    }
    instruction = style_instructions.get(summary_style, style_instructions["concise"])

    prompt = (
        f"You are a visual analysis assistant. Based on the following automated "
        f"image analysis results, {instruction}\n\n"
        f"{analysis_parts}\n\n"
        f"Summarize:"
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=1024,
        ),
    )

    return response.text.strip()


def _build_analysis_context(
    labels_response: Optional[LabelDetectionResponse] = None,
    description_response: Optional[ImageDescriptionResponse] = None,
    text_response: Optional[TextDetectionResponse] = None,
    safety_response: Optional[SafetyModerationResponse] = None,
) -> str:
    """Build a text context block from all analysis responses."""
    parts = []

    if labels_response and labels_response.labels:
        label_lines = [
            f"  - {lbl.name} ({lbl.confidence:.1f}%)"
            for lbl in labels_response.labels
        ]
        parts.append("### Detected Objects/Labels\n" + "\n".join(label_lines))

    if description_response and description_response.descriptions:
        desc_lines = [
            f"  - {desc.text} ({desc.confidence:.1f}%)"
            for desc in description_response.descriptions
        ]
        parts.append("### Image Descriptions\n" + "\n".join(desc_lines))

    if text_response and text_response.detected_texts:
        text_lines = [
            f"  - \"{txt.text}\" ({txt.confidence:.1f}%)"
            for txt in text_response.detected_texts
        ]
        parts.append("### Detected Text\n" + "\n".join(text_lines))

    if safety_response:
        if safety_response.is_safe:
            parts.append("### Safety Assessment\nImage is SAFE — no sensitive content detected.")
        else:
            safety_lines = [
                f"  - {cat.category} ({cat.confidence:.1f}%, severity: {cat.metadata.get('severity', 'unknown')})"
                for cat in safety_response.moderation_labels
            ]
            parts.append(
                f"### Safety Assessment\n"
                f"Image flagged as UNSAFE (severity: {safety_response.highest_severity})\n"
                + "\n".join(safety_lines)
            )

    return "\n\n".join(parts) if parts else "No analysis data provided."


def summarize_visual_analysis_json(
    labels_response: Optional[LabelDetectionResponse] = None,
    description_response: Optional[ImageDescriptionResponse] = None,
    text_response: Optional[TextDetectionResponse] = None,
    safety_response: Optional[SafetyModerationResponse] = None,
    model: str = "gemini-2.0-flash",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Summarize visual analysis results and return as structured JSON using Gemini.

    Args:
        labels_response: Output from detect_image_labels.
        description_response: Output from describe_image.
        text_response: Output from detect_image_text.
        safety_response: Output from score_image_safety.
        model: Gemini model identifier.
        api_key: Google API key override.

    Returns:
        Dictionary with structured summary fields.
    """
    key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set")

    client = genai.Client(api_key=key)

    analysis_parts = _build_analysis_context(
        labels_response,
        description_response,
        text_response,
        safety_response,
    )

    prompt = (
        f"Analyze the following image analysis results and return a JSON object with "
        f"keys: 'overall_description', 'key_objects', 'detected_text', 'safety_status', "
        f"and 'confidence_score'. Only output valid JSON.\n\n"
        f"{analysis_parts}"
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=512,
            response_mime_type="application/json",
        ),
    )

    try:
        return json.loads(response.text.strip())
    except json.JSONDecodeError:
        return {"raw_summary": response.text.strip()}
