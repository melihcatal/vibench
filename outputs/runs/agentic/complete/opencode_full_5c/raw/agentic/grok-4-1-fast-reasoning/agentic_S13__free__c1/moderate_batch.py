import os
import openai
from typing import Dict, Any, List


def moderate_batch(texts: List[str]) -> List[Dict[str, Any]]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="text-moderation-latest", input=texts)
    return [
        {
            "flagged": r.flagged,
            "scores": dict(r.category_scores),
            "violated_categories": [c.category for c in r.categories if c.blocked],
        }
        for r in response.results
    ]
