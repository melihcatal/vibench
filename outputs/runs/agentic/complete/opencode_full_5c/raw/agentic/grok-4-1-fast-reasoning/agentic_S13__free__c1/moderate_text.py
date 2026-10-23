import os
import openai
from typing import Dict, Any, List


def moderate_text(text: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="text-moderation-latest", input=text)
    result = response.results[0]
    violated_categories = [c.category for c in result.categories if c.blocked]
    return {
        "flagged": result.flagged,
        "scores": dict(result.category_scores),
        "violated_categories": violated_categories,
    }
