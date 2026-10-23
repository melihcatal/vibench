from typing import List


def summarize_moderation(decisions: List[dict]) -> str:
    """Summarizes moderation results for downstream pipelines.

    Args:
        decisions (List[dict]): List from moderation services each containing {
            'message': original_text, 'severity': <LEVEL>, 'passes': bool }

    Returns:
        str: Human‑readable summary containing counts and brief per‑message flags.
    """
    low = sum(1 for d in decisions if d["severity"] == "LOW")
    medium = sum(1 for d in decisions if d["severity"] == "MEDIUM")
    high = sum(1 for d in decisions if d["severity"] == "HIGH")
    total = len(decisions)
    summary = f"Moderation summary: {total} messages processed – LOW: {low}, MEDIUM: {medium}, HIGH: {high}.\n"
    if high:
        message_bodies = [
            d["message"][:50] + ("..." if len(d["message"]) > 50 else "")
            for d in decisions
            if d["severity"] == "HIGH"
        ]
        summary += "High‑severity examples:\n" + "\n".join(message_bodies) + "\n"
    return summary
