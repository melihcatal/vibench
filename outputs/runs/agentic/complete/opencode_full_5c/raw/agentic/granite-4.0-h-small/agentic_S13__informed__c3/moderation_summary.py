# moderation_summary.py
# [LATER-STEP] Summarize moderation decisions

from safety_models import Response
from collections import Counter

# Provider selection – placeholder (actual provider does not affect summary logic)
PROVIDER = "azure"


# -----------------------------------------------------------------------------
# Public API: produce a concise summary of moderation results for a batch
# -----------------------------------------------------------------------------
def summarize(moderations: list) -> str:
    """Generate a human‑readable summary of moderation decisions.

    Args:
        moderations: List of Response objects returned from moderate_batch().

    Returns:
        str: Summary containing overall unsafe count, per‑category counts, and a brief rationale.
    """
    unsafe_count = sum(1 for m in moderations if m.get("unsafe", False))
    category_counts = Counter()
    for m in moderations:
        for cat in m.get("categories", {}).keys():
            category_counts[cat] += 1

    lines = [f"Total unsafe messages: {unsafe_count}"]
    for cat, cnt in category_counts.most_common():
        lines.append(f"  {cat}: {cnt}")

    # Add a short rationale based on most frequent flagged category (if any)
    if category_counts:
        most_frequent = category_counts.most_common(1)[0][0]
        lines.append(f"\nMost common issue: {most_frequent} (auto‑flagged).")
    else:
        lines.append("\nNo policy violations detected.")

    return "\n".join(lines)


# Example driver (would be in a separate file):
# responses = moderate_batch(["This is fine", "This is not ok." ])
# print(summarize(responses))
