# redact_unsafe.py
# [SAME-SCENARIO] Flags or redacts unsafe spans from text

import re
from safety_client import parse_response
from safety_models import Response

# Provider selection – the concrete service used (kept for visibility)
PROVIDER = (
    "azure"  # Azure AI Content Safety (REST) – can be swapped for another provider
)


# -----------------------------------------------------------------------------
# Public API: redact unsafe spans from a single piece of text
# -----------------------------------------------------------------------------
def redact_unsafe(text: str) -> str:
    """Replace unsafe portions flagged by moderation with a placeholder.

    Args:
        text: The original user message.

    Returns:
        Text with any unsafe spans replaced by '[REDACTED]'.
    """
    # Moderate the text to obtain category details
    moderation = moderate_text(text)
    # If the content is deemed unsafe, replace flagged spans with placeholders
    if moderation.get("unsafe", False):
        # Simple heuristic: redact any word that appears in a detected category name
        # In a real implementation you would use the detailed spans returned by the provider
        for category in moderation.get("categories", {}):
            # Very simplistic placeholder; replace with provider-provided offsets when available
            pattern = r"\b" + re.escape(category) + r"\b"
            text = re.sub(pattern, "[REDACTED]", text, flags=re.IGNORECASE)
    # If no unsafe content was detected, return the original text unchanged
    return text if moderation.get("unsafe", False) else text


# -----------------------------------------------------------------------------
# Helper (internal) to illustrate usage in a batch context
# -----------------------------------------------------------------------------
def redact_batch(texts: list) -> list:
    """Apply redaction to multiple texts.

    Args:
        texts: List of messages.

    Returns:
        List of redacted messages.
    """
    return [redact_unsafe(t) for t in texts]


# NOTE: In production you would call the moderation helper
# defined in moderate_text.py to obtain accurate spans from the
# provider's response. Then replace the actual spans instead of simple
# word replacement shown above.
