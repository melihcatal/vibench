from typing import Dict, Any

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


def profile_moderation(profile_text: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.moderations.create(
        model=OPENAI_MODEL,
        input=profile_text,
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
