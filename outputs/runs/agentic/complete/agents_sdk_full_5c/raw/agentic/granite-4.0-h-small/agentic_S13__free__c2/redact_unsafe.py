import re
from safety_client import safety_client

def redact_unsafe(text: str, placeholder: str = '[REDACTED]') -> str:
    """Flag or redact unsafe spans from the input text.

    This naive example treats the whole message as a span. Replace with a more
    granular approach as needed.
    """
    if moderate_text(text):
        return placeholder
    return text
