# moderation_summary.py
# LATER-STEP implementation
# Summarize moderation decisions from multiple messages

from typing import List, Dict


def generate_summary(moderations: List[Dict[str, Any]]) -> str:
    """Create a concise textual summary of moderation outcomes.

    Each element of `moderations` is the raw response from a concrete provider (e.g., Alibaba).
    The function aggregates counts of allowed vs flagged messages and lists categories flagged.
    """
    allowed = 0
    flagged = 0
    flagged_categories = set()
    for mod in moderations:
        # Assume response contains a boolean 'passed' or a 'score' dict; adjust as needed
        if mod.get("passed") or not mod.get("scores"):
            allowed += 1
        else:
            flagged += 1
            # Collect all categories that exceeded thresholds
            flagged_categories.update(mod.get("scores", {}).keys())
    summary = (
        f"Total messages: {len(moderations)}\nAllowed: {allowed}\nFlagged: {flagged}"
    )
    if flagged_categories:
        summary += f"\nCategories flagged: {', '.join(sorted(flagged_categories))}"
    return summary


# Example usage (not run):
# moderations = [response1, response2, ...]
# print(generate_summary(moderations))
