import os
import json
from typing import Dict, Any, List
import anthropic


def summarize_visual_analysis(
    labels: List[Dict[str, Any]],
    description: str,
    text_detection: Dict[str, Any],
    safety_score: Dict[str, Any],
    api_key: str = None,
) -> str:
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")

    client = anthropic.Anthropic(api_key=api_key)

    analysis_data = {
        "labels": labels[:10],
        "description": description,
        "detected_text": text_detection.get("full_text", ""),
        "safety_assessment": safety_score.get("safe_search_annotation", {}),
        "is_safe": safety_score.get("is_safe", False),
    }

    prompt = f"""You are an image analysis assistant. Summarize the following visual analysis results in a concise paragraph.

Analysis Data:
{json.dumps(analysis_data, indent=2)}

Provide a 3-4 sentence summary that:
1. Describes the main content of the image based on the labels and description
2. Mentions any significant text found in the image
3. Notes the safety assessment results
4. Provides an overall assessment of the image content

Summary:"""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


def summarize_multiple_images(
    image_analyses: List[Dict[str, Any]], api_key: str = None
) -> str:
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""You are an image analysis assistant. Summarize the following collection of image analyses.

Number of images analyzed: {len(image_analyses)}

Analysis Data:
{json.dumps(image_analyses, indent=2)}

Provide a comprehensive summary that:
1. Gives an overview of the types of images analyzed
2. Highlights common themes or patterns across the images
3. Notes any safety concerns found
4. Provides insights about the overall image collection

Summary:"""

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text
