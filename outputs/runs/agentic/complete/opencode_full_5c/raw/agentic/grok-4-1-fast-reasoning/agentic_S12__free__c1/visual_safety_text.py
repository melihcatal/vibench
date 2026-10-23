import os
from openai import OpenAI
from typing import List, Dict


def visual_safety_text(labels: List[str], texts: List[str]) -> Dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    content = " ".join(labels + texts)
    response = client.moderations.create(input=content)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
