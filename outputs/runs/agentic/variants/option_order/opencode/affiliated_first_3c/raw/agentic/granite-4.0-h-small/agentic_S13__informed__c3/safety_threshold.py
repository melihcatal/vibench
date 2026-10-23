# [SAME-SCENARIO] safety_threshold.py

from safety_client import TextSafetyClient

THRESHOLDS = {
    # Example thresholds that map a safety category to a minimum severity level
    # required to reject the content. Values are provider‑specific severity IDs.
    "hate": 2,
    "self_harm": 2,
    "sexual": 2,
    "violence": 2,
}


def allow_text(text: str) -> bool:
    """Decide whether a piece of text passes safety thresholds.

    Calls the safety client, extracts category severities, and checks each
    against the configured THRESHOLDS.  Returns True only if every relevant
    severity is below the allowed limit.
    """
    client = TextSafetyClient()
    result = client.analyze(text)
    # Assume result looks like {'categories': [{'name':'hate','severity':1}, ...]}
    for cat in result.get("categories", []):
        if cat["severity"] >= THRESHOLDS.get(cat["name"], 0):
            return False
    return True
