import os
from typing import Dict, Any, List

from openai import OpenAI
from vision_models import Label, TextRegion, ImageDescription


def summarize_visual_analysis(
    labels: List[Label],
    text_regions: List[TextRegion],
    image_description: ImageDescription,
    model: str = "gpt-4o",
) -> str:
    """
    Summarizes visual analysis results using OpenAI's GPT model.

    Args:
        labels: List of detected labels.
        text_regions: List of detected text regions.
        image_description: Visual description of the image.
        model: OpenAI model to use for summarization.

    Returns:
        A summarized visual analysis of the image.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key must be provided.")

    client = OpenAI(api_key=api_key)

    label_text = ", ".join([label.name for label in labels])
    text_region_text = ", ".join([region.text for region in text_regions])

    prompt = (
        f"Summarize the following visual analysis of an image:\n"
        f"Description: {image_description.description}\n"
        f"Detected Labels: {label_text}\n"
        f"Detected Text: {text_region_text}\n"
        f"Provide a concise summary in 2-3 sentences."
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        raise Exception(f"OpenAI error: {e}")
