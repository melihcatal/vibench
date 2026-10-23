import os
from typing import Dict, Any, List
import anthropic


def summarize_visual_analysis(
    labels: List[Dict[str, Any]],
    text_detections: List[Dict[str, Any]],
    description: str,
    safety_score: Dict[str, Any],
) -> str:
    """
    Summarize visual analysis results using Anthropic Claude.

    Args:
        labels: List of detected labels
        text_detections: List of detected text
        description: Image description
        safety_score: Safety assessment

    Returns:
        Summary text
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    label_text = ", ".join([label["name"] for label in labels[:10]])
    text_content = ", ".join([detection["text"] for detection in text_detections[:5]])

    prompt = f"""Summarize the visual analysis of an image:

Image Description: {description}

Detected Labels: {label_text}
Detected Text: {text_content}
Safety Assessment: {"Safe" if safety_score["is_safe"] else "Not safe - contains: " + ", ".join([label["name"] for label in safety_score["moderation_labels"]])}

Provide a concise 2-3 sentence summary of what the image contains and any notable findings."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text
