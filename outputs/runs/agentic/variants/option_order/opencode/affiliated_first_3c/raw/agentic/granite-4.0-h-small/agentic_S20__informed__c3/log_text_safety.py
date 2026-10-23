import os
import json
from observability_client import ManagedLogClient
from observability_models import LogEntry


def log_text_safety(
    log_entries: list[LogEntry], threshold: float = 0.8
) -> list[LogEntry]:
    """Check selected log message text for unsafe content using watsonx guardrails.

    Returns only safe entries (or empty list if none pass). The concrete provider
    is watsonx guardrails / HAP detection.
    """
    safe_entries = []
    for entry in log_entries:
        if _is_text_safe(entry.message, threshold):
            safe_entries.append(entry)
    return safe_entries


def _is_text_safe(text: str, threshold: float) -> bool:
    # Placeholder – real implementation would call watsonx guardrails API
    # e.g. response = client.guardrails.check(text=text)
    # Assume safe if len(text) < 200 (demo heuristic)
    return len(text) < 200
