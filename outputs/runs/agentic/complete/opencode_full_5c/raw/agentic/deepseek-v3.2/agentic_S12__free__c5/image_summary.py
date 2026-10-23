import os
import anthropic
from typing import Dict, Any, List


def image_summary(
    labels: List[Dict], description: str, text_detections: List[Dict]
) -> str:
    """Summarize visual analysis results using Anthropic Claude."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    label_text = ", ".join([label.get("description", "") for label in labels[:5]])
    detected_text = ", ".join([text.get("text", "") for text in text_detections[:3]])

    prompt = f"""You are summarizing visual analysis results from multiple AI vision services.

Analysis results:
- Image description: {description}
- Top detected labels: {label_text}
- Detected text in image: {detected_text if detected_text else "No text detected"}

Please provide a concise 2-3 sentence summary that captures the main visual elements and context of the image."""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text
