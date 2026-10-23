import openai
import os
from typing import Dict, Any


def unsafe_copy_check(text: str) -> Dict[str, Any]:
    """
    Check translated copy for unsafe content using OpenAI Moderation API.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="text-moderation-latest", input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
