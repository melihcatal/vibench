import os
from watsonx_ai import APIClient

def visual_safety_text(text_lines: list) -> bool:
    """Check generated visual labels/descriptions for unsafe text using watsonx guardrails.
    Returns True if safe, False if unsafe.
    Requires environment variables: WATSONX_API_KEY, WATSONX_PROJECT_ID.
    """
    client = APIClient()
    # Simple check: send each line to guardrails endpoint (placeholder logic)
    for line in text_lines:
        resp = client.call('guardrails/check', {'text': line})
        if not resp.get('safe', True):
            return False
    return True
