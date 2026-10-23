import os
from safety_client import TextSafetyClient
from safety_models import ModerationRequest, ModerationResponse

def moderate_text(user_text: str, threshold: float = 0.5) -> bool:
    """Score a single piece of user-generated text for unsafe or policy‑violating content.

    Uses OpenAI's content‑moderation endpoint (via safety_client). Returns True if the
    text passes moderation (i.e., is considered safe).
    """
    request = ModerationRequest(text=user_text, model="content-safety-gpt-4")
    client = TextSafetyClient()
    response: ModerationResponse = client.moderate(request)
    # Identify provider by model ID used in the request.
    for result in response.results:
        if result.flagged and result.score >= threshold:
            return False  # unsafe
    return True  # safe
