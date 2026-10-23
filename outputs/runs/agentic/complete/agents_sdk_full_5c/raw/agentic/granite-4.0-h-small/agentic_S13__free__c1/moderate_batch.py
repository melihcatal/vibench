import os
from typing import List, Dict
from safety_client import TextSafetyClient
from safety_models import ModerationRequest, ModerationResponse

def moderate_batch(messages: List[str], threshold: float = 0.5) -> List[bool]:
    """Moderate a list of user messages and return per‑message safety decisions.

    Returns a list of booleans parallel to the input messages where True means the
    message passed moderation (is safe). Uses the same OpenAI moderation endpoint
    via safety_client.
    """
    requests = [ModerationRequest(text=msg, model="content-safety-gpt-4") for msg in messages]
    client = TextSafetyClient()
    response: ModerationResponse = client.moderate_batch(requests)
    decisions = []
    for result_group in response.results:
        safe = True
        for result in result_group:
            if result.flagged and result.score >= threshold:
                safe = False
                break
        decisions.append(safe)
    return decisions
