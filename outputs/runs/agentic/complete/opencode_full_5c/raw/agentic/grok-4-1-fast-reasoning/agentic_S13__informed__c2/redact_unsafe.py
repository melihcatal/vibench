from safety_client import redact_text
from typing import Dict, Any


def redact_unsafe(text: str) -> Dict[str, Any]:
    """
    Flags or redacts unsafe spans from text using Tisane API.
    """
    return redact_text(text)
