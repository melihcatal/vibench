import os
import anthropic
from typing import Dict, Any, List


def summarize_visual_analysis(
    labels: List[Dict[str, Any]],
    description: Dict[str, Any],
    text_detections: List[Dict[str, Any]],
    safety_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Summarize visual analysis results using Anthropic Claude.

    Args:
        labels: List of detected labels
        description: Image description
        text_detections: List of detected text
        safety_result: Safety analysis result

    Returns:
        Dictionary containing summary and analysis
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    labels_text = ", ".join([label.get("description", "") for label in labels[:5]])
    description_text = description.get("description", "")

    text_summary = ""
    if text_detections:
        text_items = [text.get("text", "")[:50] + "..." for text in text_detections[:3]]
        text_summary = f"Contains text: {', '.join(text_items)}"

    safety_status = "safe" if safety_result.get("is_safe", False) else "needs review"

    prompt = f"""You are an image analysis assistant. Summarize the following image analysis results:

Image Description: {description_text}

Detected Objects/Labels: {labels_text}

{text_summary}

Safety Status: {safety_status}

Provide a concise 2-3 sentence summary of what this image contains and any notable findings."""

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        return {
            "summary": summary_text,
            "provider": "anthropic-claude-3-sonnet",
            "model": "claude-3-sonnet-20240229",
            "labels_count": len(labels),
            "text_detected": len(text_detections) > 0,
            "is_safe": safety_result.get("is_safe", False),
        }
    except Exception as e:
        raise Exception(f"Anthropic API error: {str(e)}")
