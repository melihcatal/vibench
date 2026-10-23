import os
from typing import Dict, List
from openai import OpenAI
from vision_models import LabelDetectionResponse, ImageDescriptionResponse


def summarize_visual_analysis(
    labels: LabelDetectionResponse,
    description: ImageDescriptionResponse
) -> str:
    """Summarizes visual analysis results using OpenAI GPT-4."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = (
        "Summarize the following visual analysis of an image:\n"
        f"Labels: {', '.join(labels.labels)}\n"
        f"Description: {description.description}\n"
        "Provide a concise summary in 2-3 sentences."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    return response.choices[0].message.content.strip()