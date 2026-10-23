import os
import openai
from typing import Dict, Any

def check_metric_annotation_safety(annotation_text: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        input=annotation_text,
        model="text-moderation-3.5-large"
    )
    result = response.results[0]
    flagged_categories = {cat: score for cat, score in result.category_scores.items() if score > 0.5}
    return {
        "safe": not result.flagged,
        "flagged": result.flagged,
        "categories": flagged_categories
    }
