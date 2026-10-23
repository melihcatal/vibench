import os
import openai
from typing import Dict, Any
from vision_models import LabelResult, ImageDescriptionResult, TextResult

def check_text_for_safety(text_content: str) -> Dict[str, Any]:
    """
    Checks text (e.g., generated labels, descriptions) for unsafe content
    using the OpenAI Moderation API.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.Moderation.create(
        input=text_content,
        model="text-moderation-latest" # Concrete model family/identifier
    )

    moderation_result = response["results"][0]
    return {
        "flagged": moderation_result["flagged"],
        "categories": {k: v for k, v in moderation_result["categories"].items() if v},
        "category_scores": {k: v for k, v in moderation_result["category_scores"].items() if v > 0.01},
    }
