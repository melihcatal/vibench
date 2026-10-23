from typing import Dict, Any
from vision_client import openai_client

def visual_safety_text(text: str) -> Dict[str, Any]:
    if not text:
        return {"flagged": False}
    response = openai_client.moderations.create(
        model="text-moderation-latest",
        input=text
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
