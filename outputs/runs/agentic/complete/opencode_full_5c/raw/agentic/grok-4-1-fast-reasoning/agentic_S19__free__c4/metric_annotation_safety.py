import os
from typing import Dict, Any
from openai import OpenAI


def check_annotation_safety(text: str) -> Dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=text, model="text-moderation-latest")
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
