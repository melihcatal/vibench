import os
from typing import Dict, Any, List
from anthropic import Anthropic


def image_summary(
    labels: List[str], text_detections: List[str], safety_scores: Dict[str, str]
) -> str:
    """
    Summarize visual analysis results using Anthropic Claude.

    Args:
        labels: List of detected labels
        text_detections: List of detected text
        safety_scores: Dictionary of safety scores

    Returns:
        Summary of visual analysis
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    labels_text = ", ".join(labels[:10]) if labels else "No labels detected"
    text_summary = (
        ", ".join(text_detections[:5]) if text_detections else "No text detected"
    )

    safety_summary = ""
    if safety_scores:
        unsafe_categories = []
        for category, score in safety_scores.items():
            if score in ["LIKELY", "VERY_LIKELY"]:
                unsafe_categories.append(f"{category}: {score}")

        if unsafe_categories:
            safety_summary = f"Safety concerns: {', '.join(unsafe_categories)}"
        else:
            safety_summary = "Image appears safe"

    prompt = f"""Based on the following image analysis, provide a concise summary:

Detected objects/labels: {labels_text}
Detected text: {text_summary}
Safety assessment: {safety_summary}

Provide a brief, natural language summary of what's in the image and any notable findings."""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text
