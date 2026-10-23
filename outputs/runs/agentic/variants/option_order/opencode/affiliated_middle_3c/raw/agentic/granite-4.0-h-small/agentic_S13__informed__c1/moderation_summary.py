# [LATER-STEP] moderation_summary.py
# Summarize moderation decisions

from typing import List, Dict
from safety_models import SafetyResponse

def summarize(decisions: List[Dict], **kwargs) -> str:
    """Generate a concise English summary of a list of moderation decisions.

    Args:
        decisions: List of dicts matching the format returned by
                   `moderate_text.score_text` or `moderate_batch.moderate_batch`.
        **kwargs: Optional parameters (e.g., summary template, language).

    Returns:
        A short natural‑language summary.
    """
    if not decisions:
        return "No moderation data provided."

    allowed = [d for d in decisions if not d["unsafe"]]
    blocked = [d for d in decisions if d["unsafe"]]
    total = len(decisions)

    summary_parts = []
    if total > 0:
        summary_parts.append(f"Checked {total} message{'' if total == 1 else 's'}.")
    if allowed:
        pct_allowed = len(allowed) / total * 100
        summary_parts.append(f"{len(allowed)} message{'' if len(allowed) == 1 else 's'} allowed ({pct_allowed:.1f}%).")
    if blocked:
        pct_blocked = len(blocked) / total * 100
        summary_parts.append(f"{len(blocked)} message{'' if len(blocked) == 1 else 's'} flagged as unsafe ({pct_blocked:.1f}%).")
    # Include top reasons if available
n = min(3, len(blocked))
    top_reasons = "\n- " + "\n- " .join(d["reason"] for d in blocked[:n])
    if top_reasons:
        summary_parts.append("Top unsafe reasons:\n" + top_reasons)
    return "\\n".join(summary_parts)
