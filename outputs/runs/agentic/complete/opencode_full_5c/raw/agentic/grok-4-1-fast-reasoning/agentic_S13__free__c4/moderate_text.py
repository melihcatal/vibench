import openai
import os
from typing import Dict, Any, List
from safety_models import SafetyCategory, ModerationDecision
from safety_client import get_api_key


def moderate_text(text: str) -> Dict[str, Any]:
    api_key = get_api_key("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=api_key)
    response = client.moderation.create(model="text-moderation-latest", input=text)
    result = response.results[0]
    categories = [
        SafetyCategory(category=cat, score=score)
        for cat, score in result.category_scores.items()
    ]
    flagged = result.flagged
    return {
        "input_text": text,
        "flagged": flagged,
        "categories": categories,
        "details": None,
    }
