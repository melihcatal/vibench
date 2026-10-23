import os
from openai import OpenAI
from typing import Dict, Any


def check_platform_output_safety(output: str) -> Dict[str, Any]:
    """
    Checks output safety using OpenAI Moderation API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    response = client.moderations.create(
        model="text-moderation-3.5-turbo",
        input=output,
    )
    result = response.results[0]
    return {
        "is_safe": not result.flagged,
        "flagged_categories": result.categories,
        "scores": result.category_scores,
    }
