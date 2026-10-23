from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import openai

from vision_client import OPENAI_API_BASE, VISION_MODEL_ID, get_openai_client
from vision_models import (
    DescriptionResponse,
    LabelResponse,
    SafetyResponse,
    TextDetectionResponse,
    description_response_to_dict,
    label_response_to_dict,
    safety_response_to_dict,
    text_detection_response_to_dict,
)

SUMMARY_PROMPT_TEMPLATE = """You are an image analysis summarizer. Given the following structured analysis results for a single image,
produce a concise summary (3-5 sentences) that synthesizes the key findings.

Labels detected: {labels}
Description: {description}
Text found: {text}
Safety assessment: {safety}

Provide a unified summary covering: what the image depicts, any text present, and whether it is safe for general audiences."""


def build_analysis_payload(
    labels: Optional[LabelResponse] = None,
    description: Optional[DescriptionResponse] = None,
    text_detection: Optional[TextDetectionResponse] = None,
    safety: Optional[SafetyResponse] = None,
) -> Dict[str, Any]:
    return {
        "labels": label_response_to_dict(labels) if labels else {},
        "description": description_response_to_dict(description) if description else {},
        "text_detection": text_detection_response_to_dict(text_detection)
        if text_detection
        else {},
        "safety": safety_response_to_dict(safety) if safety else {},
    }


def summarize_visual_analysis(
    labels: Optional[LabelResponse] = None,
    description: Optional[DescriptionResponse] = None,
    text_detection: Optional[TextDetectionResponse] = None,
    safety: Optional[SafetyResponse] = None,
    api_key: Optional[str] = None,
    model: str = VISION_MODEL_ID,
) -> str:
    payload = build_analysis_payload(labels, description, text_detection, safety)

    labels_str = ", ".join(
        f"{l['name']} ({l['confidence']:.2f})"
        for l in payload.get("labels", {}).get("labels", [])
    )
    desc_str = payload.get("description", {}).get(
        "description", "No description available."
    )
    text_str = payload.get("text_detection", {}).get("full_text", "No text detected.")
    safe_str = (
        "Safe"
        if payload.get("safety", {}).get("overall_safe", True)
        else "Potentially unsafe"
    )

    prompt = SUMMARY_PROMPT_TEMPLATE.format(
        labels=labels_str or "None",
        description=desc_str,
        text=text_str or "None",
        safety=safe_str,
    )

    client = get_openai_client(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You summarize image analysis results concisely.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=512,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


def generate_summary_report(
    labels: Optional[LabelResponse] = None,
    description: Optional[DescriptionResponse] = None,
    text_detection: Optional[TextDetectionResponse] = None,
    safety: Optional[SafetyResponse] = None,
    api_key: Optional[str] = None,
    model: str = VISION_MODEL_ID,
) -> Dict[str, Any]:
    summary_text = summarize_visual_analysis(
        labels, description, text_detection, safety, api_key, model
    )
    payload = build_analysis_payload(labels, description, text_detection, safety)
    payload["summary"] = summary_text
    return payload


if __name__ == "__main__":
    result = generate_summary_report()
    print(json.dumps(result, indent=2))
