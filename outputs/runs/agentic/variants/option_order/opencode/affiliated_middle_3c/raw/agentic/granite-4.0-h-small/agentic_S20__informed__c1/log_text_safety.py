import os
from observability_client import ManagedLogClient


def log_text_safety(log_entries: list, unsafe_keywords: list = None) -> list:
    """Checks selected log message text for unsafe content.

    Uses a simple keyword filter; replace with a managed service call
    (e.g., Amazon Comprehend, Watson Guardrails) for production.

    Args:
        log_entries (list): List of log dicts with a 'text' field.
        unsafe_keywords (list): Optional custom list of unsafe terms.

    Returns:
        list: Entries flagged as safe (True) or unsafe (False).
    """
    unsafe = unsafe_keywords or ["password", "secret", "key", "token"]
    client = ManagedLogClient()
    flagged = []
    for entry in log_entries:
        text = entry.get("text", "").lower()
        is_safe = not any(k in text for k in unsafe)
        flagged.append({**entry, "safe": is_safe})
    return flagged
