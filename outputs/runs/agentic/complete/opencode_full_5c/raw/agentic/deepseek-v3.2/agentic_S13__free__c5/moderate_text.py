import os
from typing import Dict, Any, Optional
from openai import OpenAI


def moderate_text(text: str) -> Dict[str, Any]:
    """
    Scores user text for unsafe or policy-violating content using OpenAI's moderation API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    response = client.moderations.create(model="text-moderation-latest", input=text)

    result = response.results[0]

    return {
        "flagged": result.flagged,
        "categories": result.categories.model_dump(),
        "category_scores": result.category_scores.model_dump(),
        "text": text,
    }
