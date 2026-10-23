import os
from openai import OpenAI
from typing import Dict, Any
from safety_models import ModerationResult


def moderate_text(text: str) -> ModerationResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="text-moderation-latest", input=text)
    moderation_result = response.results[0]
    categories = dict(moderation_result.category_scores)
    return {
        "input_text": text,
        "flagged": moderation_result.flagged,
        "categories": categories,
        "rationale": None,
    }
