from typing import List, Dict

def summarize_moderation(decisions: List[bool], reasons: List[Dict]) -> str:
    """Create a concise summary of moderation decisions for a batch of messages.

    decisions: list of booleans where True indicates the message passed moderation.
    reasons: parallel list of dictionaries containing the moderation rationale from
             the provider (e.g., categories and scores).
    Returns a human‑readable one‑line summary.
    """
    safe_count = sum(decisions)
    unsafe_count = len(decisions) - safe_count
    summary = f"Moderated {len(decisions)} messages: {safe_count} safe, {unsafe_count} unsafe."
    if unsafe_count:
        summary += " Unsafe messages detected."
    return summary
