import os
from openai import OpenAI
from typing import List, Dict


def visual_safety_text(texts: List[str]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    input_text = "\\n".join(texts)
    response = client.moderations.create(
        model="text-moderation-latest", input=input_text
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": {k: float(v) for k, v in result.category_scores.items()},
    }
