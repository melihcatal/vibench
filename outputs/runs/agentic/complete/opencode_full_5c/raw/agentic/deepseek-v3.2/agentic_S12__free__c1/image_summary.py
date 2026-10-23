import os
import json
from typing import Dict, Any
from anthropic import Anthropic
from vision_client import get_anthropic_api_key


def summarize_visual_analysis(analysis_results: Dict[str, Any]) -> str:
    """Summarize visual analysis results using Anthropic Claude."""
    api_key = get_anthropic_api_key()
    client = Anthropic(api_key=api_key)

    analysis_text = json.dumps(analysis_results, indent=2)

    prompt = f"""You are an expert visual analysis summarizer. Given the following image analysis results, provide a concise, informative summary.

Analysis Results:
{analysis_text}

Please provide a summary that includes:
1. Main objects/labels detected
2. Key text found in the image (if any)
3. Safety assessment
4. Overall description of the image content

Keep the summary under 200 words."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


def get_anthropic_api_key() -> str:
    """Get Anthropic API key."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return api_key


if __name__ == "__main__":
    # Example usage
    sample_analysis = {
        "labels": [
            {"description": "dog", "score": 0.95},
            {"description": "park", "score": 0.87},
            {"description": "grass", "score": 0.82},
        ],
        "description": "A brown dog playing in a grassy park",
        "text_detections": [{"text": "Welcome", "confidence": 0.91}],
        "safety_score": {
            "flagged": False,
            "categories": {"violence": False, "hate": False, "sexual": False},
        },
    }

    summary = summarize_visual_analysis(sample_analysis)
    print("Analysis Summary:")
    print(summary)
