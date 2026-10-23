import os
from safety_client import SafetyClient


def moderate_batch(messages: list[str]) -> list[bool]:
    """Moderate a batch of user messages and return per‑message unsafe decisions.

    Returns a list of booleans matching the input order: True if unsafe, False otherwise.
    """
    client = SafetyClient()
    responses = client.batch_moderate(messages)
    return [resp["unsafe"] for resp in responses]
