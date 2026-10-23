from safety_client import get_openai_client
from safety_models import normalize_openai, ModerationDecision
from typing import List


def moderate_text(text: str) -> ModerationDecision:
    client = get_openai_client()
    if client is None:
        raise ValueError("OpenAI API key not configured")
    response = client.moderations.create(model="text-moderation-latest", input=text)
    result = response.results[0]
    return normalize_openai(result)
