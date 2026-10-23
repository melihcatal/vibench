from safety_client import get_openai_client
from safety_models import normalize_openai, ModerationDecision
from typing import List


def moderate_batch(texts: List[str]) -> List[ModerationDecision]:
    client = get_openai_client()
    if client is None:
        raise ValueError("OpenAI API key not configured")
    response = client.moderations.create(model="text-moderation-latest", input=texts)
    return [normalize_openai(result) for result in response.results]
