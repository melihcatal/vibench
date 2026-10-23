import os
from openai import OpenAI
from typing import Dict

def moderate_text(text: str) -> Dict:
    """
    Scores user text for unsafe or policy-violating content using OpenAI Moderation API.
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(
        model="text-moderation-latest",
        input=text
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores)
    }
