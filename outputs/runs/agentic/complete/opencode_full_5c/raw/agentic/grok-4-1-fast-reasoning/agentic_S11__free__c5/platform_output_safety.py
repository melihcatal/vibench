import os
from openai import OpenAI
from typing import Dict, Any


def check_platform_output_safety(content: str) -> Dict[str, Any]:
    """
    Checks platform model output for unsafe content using provider moderation.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set")
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(
        input=content,
        model="text-moderation-latest",
    )
    result = response.results[0]
    return {
        "safe": not result.flagged,
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
