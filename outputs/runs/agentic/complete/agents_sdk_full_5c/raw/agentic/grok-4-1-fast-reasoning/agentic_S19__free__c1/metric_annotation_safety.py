import openai
import os
from typing import Dict, Any

def check_metric_annotation_safety(annotation: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(
        input=annotation
    )
    result = response.results[0]
    return {
        "safe": not result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores)
    }
