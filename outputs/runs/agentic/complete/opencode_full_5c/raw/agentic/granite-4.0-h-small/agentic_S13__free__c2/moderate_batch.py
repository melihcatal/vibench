# SAME-SCENARIO: Moderate a batch of user messages

from safety_client import get_client


def moderate_batch(messages: list[str], threshold: float = 0.5) -> list[bool]:
    """Return list of booleans indicating unsafe text for each message.

    Uses OpenAI Moderation endpoint.
    """
    client = get_client()
    response = client.moderations.create(input=messages)
    return [result["flagged"] for result in response["results"]]
