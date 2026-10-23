import os
import anthropic
from typing import Dict, Any, List


def summarize_visual_analysis(
    labels: List[Dict[str, Any]],
    description: str,
    text_detections: List[Dict[str, Any]],
    safety_scores: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Summarize visual analysis results using Anthropic Claude.

    Args:
        labels: List of detected labels
        description: Generated image description
        text_detections: List of detected text items
        safety_scores: Safety analysis results

    Returns:
        Dictionary containing the summary and analysis
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    label_text = ", ".join([label.get("description", "") for label in labels[:10]])
    detected_text = ", ".join([text.get("text", "") for text in text_detections[:5]])

    prompt = f"""You are an image analysis assistant. Summarize the following visual analysis results:

Image Description: {description}

Detected Objects/Labels: {label_text}

Detected Text: {detected_text}

Safety Assessment:
- Adult content: {safety_scores.get("is_adult_content", False)} (score: {safety_scores.get("adult_score", 0.0):.3f})
- Racy content: {safety_scores.get("is_racy_content", False)} (score: {safety_scores.get("racy_score", 0.0):.3f})
- Gory content: {safety_scores.get("is_gory_content", False)} (score: {safety_scores.get("gore_score", 0.0):.3f})

Provide a concise summary (2-3 sentences) of what the image contains and any notable findings."""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )

    summary = response.content[0].text

    return {
        "summary": summary.strip(),
        "model": "claude-3-sonnet-20240229",
        "provider": "anthropic",
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }


if __name__ == "__main__":
    # Example usage
    sample_labels = [
        {"description": "mountain", "score": 0.95},
        {"description": "sky", "score": 0.92},
    ]
    sample_description = "A scenic mountain landscape with blue sky"
    sample_text = [{"text": "Welcome", "confidence": 0.98}]
    sample_safety = {
        "is_adult_content": False,
        "adult_score": 0.01,
        "is_racy_content": False,
        "racy_score": 0.02,
        "is_gory_content": False,
        "gore_score": 0.01,
    }

    try:
        summary = summarize_visual_analysis(
            sample_labels, sample_description, sample_text, sample_safety
        )
        print(f"Summary: {summary['summary']}")
        print(f"Model: {summary['model']}")
        print(f"Provider: {summary['provider']}")
    except Exception as e:
        print(f"Error: {e}")
