import os
import openai
from typing import Dict, Any


def check_metric_annotation_safety(annotation: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.beta.moderations.create(
        model="moderation-latest", input=annotation
    )
    result = response.results[0]
    return {
        "is_safe": not result.flagged,
        "flagged_categories": result.categories,
        "category_scores": result.category_scores,
    }
