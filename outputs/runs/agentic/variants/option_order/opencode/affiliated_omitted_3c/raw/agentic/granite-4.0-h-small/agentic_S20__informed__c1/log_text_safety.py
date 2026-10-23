import os
from observability_client import get_ingestion_client
from observability_models import LogEvent


def log_text_safety(events: list[LogEvent], unsafe_terms: list[str]) -> list[LogEvent]:
    """Checks selected log message text for unsafe content.

    Returns a filtered list containing only events whose message does NOT include
    any term from `unsafe_terms` (case‑insensitive). The underlying provider may
    also be invoked for moderation, but this helper demonstrates a local safeguard.
    """
    client = get_ingestion_client()  # placeholder – moderation could be delegated
    safe_events = []
    lower_terms = [t.lower() for t in unsafe_terms]
    for evt in events:
        msg_lower = evt["message"].lower()
        if not any(term in msg_lower for term in lower_terms):
            safe_events.append(evt)
    return safe_events
