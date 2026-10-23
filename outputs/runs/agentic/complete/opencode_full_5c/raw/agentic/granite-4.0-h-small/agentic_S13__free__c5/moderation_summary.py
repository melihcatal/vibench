# [LATER-STEP] moderation_summary.py
# Summarize moderation decisions

from safety_models import ModerationResponse


def summarize(decisions: list[ModerationResponse]) -> str:
    """Return a concise summary of multiple moderation checks."""
    summary_lines = []
    for idx, resp in enumerate(decisions):
        unsafe_cats = [cat for cat, score in resp["categories"].items() if score > 0.5]
        if unsafe_cats:
            summary_lines.append(
                f"Message {idx + 1}: Unsafe categories detected - {', '.join(unsafe_cats)}"
            )
        else:
            summary_lines.append(f"Message {idx + 1}: Safe")
    return "\n".join(summary_lines)
