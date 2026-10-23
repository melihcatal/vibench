from typing import Any, Dict

import openai

OPENAI_MODEL = "gpt-4.1-mini"


def claims_moderation(text: str, api_key: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=api_key)
    result = client.moderations.create(model="omni-moderation-latest", input=text)
    moderated = result.results[0] if result.results else None
    return {
        "flagged": bool(getattr(moderated, "flagged", False)),
        "categories": getattr(moderated, "categories", {}),
        "category_scores": getattr(moderated, "category_scores", {}),
        "model": "omni-moderation-latest",
    }
