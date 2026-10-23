import os
from openai import OpenAI
from safety_client import load_openai_client
from safety_models import ModerationResult

def moderate_text(text: str) -> ModerationResult:
    client = load_openai_client()
    response = client.moderations.create(input=text, model="text-moderation-latest")
    
    result = response.results[0]
    categories = {k: v for k, v in result.categories.__dict__.items() if not k.startswith('_')}
    category_scores = {k: v for k, v in result.category_scores.__dict__.items() if not k.startswith('_')}

    return ModerationResult(
        is_flagged=result.flagged,
        categories=categories,
        category_scores=category_scores
    )
