from typing import List
from safety_client import get_openai_client
from safety_models import OpenAIModerationResponse


def moderate_batch(texts: List[str]) -> List[OpenAIModerationResponse]:
    """
    Moderates a batch of user messages and returns per-message decisions
    using OpenAI's Moderation API.
    """
    client = get_openai_client()

    # The OpenAI Python SDK currently moderates a list of inputs and returns a single response object.
    # We will adapt this to the expected output format.
    response = client.moderations.create(input=texts)

    # Reconstruct a list of responses to match the function signature,
    # even though OpenAI returns one object for a batch.
    return [
        OpenAIModerationResponse(id=response.id, model=response.model, results=[result])
        for result in response.results
    ]
