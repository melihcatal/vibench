import os
from openai import OpenAI
from typing import List
from vision_client import get_openai_client
from vision_models import ModerationResult

def check_text_safety(texts: List[str]) -> List[ModerationResult]:
    client = get_openai_client()

    moderation_results = []
    for text in texts:
        response = client.moderations.create(input=text, model="text-moderation-latest")
        
        result = response.results[0]
        moderation_results.append(
            ModerationResult(
                flagged=result.flagged,
                categories={k: getattr(result.categories, k) for k in result.categories.__dict__ if not k.startswith('_')},
                category_scores={k: getattr(result.category_scores, k) for k in result.category_scores.__dict__ if not k.startswith('_')}
            )
        )
    return moderation_results