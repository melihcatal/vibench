import os
from typing import Dict, Any, List
import anthropic
from vision_client import get_openai_api_key
from vision_models import ImageAnalysisResult


def summarize_visual_analysis(
    labels: List[Dict[str, Any]],
    description: str,
    detected_text: List[Dict[str, Any]],
    safety_score: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Summarize visual analysis results using Anthropic Claude.

    Args:
        labels: List of detected labels
        description: Image description
        detected_text: List of detected text
        safety_score: Safety analysis results

    Returns:
        Dictionary containing summary and insights
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    labels_text = ", ".join([label.get("description", "") for label in labels[:10]])
    detected_text_str = ", ".join([text.get("text", "") for text in detected_text[:5]])

    prompt = f"""
    Summarize the visual analysis of an image with the following components:
    
    1. Detected Labels: {labels_text}
    2. Image Description: {description}
    3. Detected Text: {detected_text_str}
    4. Safety Score: Adult={safety_score.get("adult_score", 0)}, 
       Racy={safety_score.get("racy_score", 0)}, 
       Gore={safety_score.get("gore_score", 0)}
    
    Provide a concise summary (2-3 sentences) that captures:
    - Main subjects and themes
    - Any notable text content
    - Safety assessment
    - Overall impression
    """

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    summary_text = response.content[0].text

    return {
        "summary": summary_text,
        "provider": "anthropic-claude",
        "model": "claude-3-sonnet-20240229",
        "components_analyzed": ["labels", "description", "text", "safety"],
        "summary_length": len(summary_text),
    }
