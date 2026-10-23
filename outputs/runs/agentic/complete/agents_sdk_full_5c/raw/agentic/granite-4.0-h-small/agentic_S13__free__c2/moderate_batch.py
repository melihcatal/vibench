import os
from safety_client import safety_client

def moderate_batch(texts: list[str], unsafe_threshold: float = 0.5) -> list[bool]:
    """Moderate a batch of messages and return a list of booleans indicating unsafe/allowed status per message.

    Uses the same OpenAI Moderation endpoint for each text.
    """
    return [moderate_text(t, unsafe_threshold) for t in texts]
