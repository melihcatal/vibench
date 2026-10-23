import re
from safety_client import TextSafetyClient
from safety_models import ModerationRequest, ModerationResponse

def redact_unsafe(text: str, replacement: str = "[REDACTED]") -> str:
    """Flag or redact unsafe spans from user text based on moderation results.

    Performs a single moderation request and replaces any flagged span with the
    replacement string. The provider signal is the model ID used in the request.
    """
    request = ModerationRequest(text=text, model="content-safety-gpt-4")
    client = TextSafetyClient()
    response: ModerationResponse = client.moderate(request)
    # Simple approach: replace each flagged span with replacement. In a real
    # implementation you might retain position info from the provider.
    for result in response.results[0]:  # assuming one top‑level result block
        if result.flagged:
            # Naive replacement of the exact flagged text
            text = text.replace(result.flagged_text, replacement)
    return text
