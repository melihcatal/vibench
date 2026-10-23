from typing import List
from safety_client import get_openai_client
from safety_models import ModerationResponse


def moderate_batch(texts: List[str]) -> ModerationResponse:
    """
    Moderates a batch of user messages and returns per-message decisions using OpenAI.
    """
    client = get_openai_client()
    response = client.moderations.create(input=texts, model="text-moderation-latest")

    return ModerationResponse.model_validate(response.dict())
