import os
import openai
from vision_client import get_openai_client
from typing import Dict, Any


def summarize_visual_analysis(analysis_results: Dict[str, Any]) -> str:
    """Summarize visual analysis results using OpenAI GPT-4."""
    client = get_openai_client()

    labels_text = ", ".join(
        [label["description"] for label in analysis_results.get("labels", [])[:10]]
    )
    safety_status = (
        "safe"
        if analysis_results.get("safety_scores", {}).get("is_safe", True)
        else "unsafe"
    )
    has_text = (
        "contains text"
        if analysis_results.get("detected_text", {}).get("text")
        else "no text detected"
    )
    description = analysis_results.get("description", "No description available")

    prompt = f"""
    Summarize the following image analysis results in a concise paragraph:
    
    Image Analysis:
    - Detected objects/labels: {labels_text}
    - Safety status: {safety_status}
    - Text detection: {has_text}
    - Generated description: {description}
    
    Provide a brief summary that captures the key visual elements and assessment.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes image analysis results.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.7,
    )

    summary = response.choices[0].message.content
    return summary.strip()
