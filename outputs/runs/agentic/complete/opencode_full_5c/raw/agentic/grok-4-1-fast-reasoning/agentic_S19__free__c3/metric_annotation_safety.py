import os
from openai import OpenAI
from typing import Dict, Any


def check_annotation_safety(annotation_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        input=annotation_text, model="text-moderation-latest"
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "scores": dict(result.category_scores),
    }
