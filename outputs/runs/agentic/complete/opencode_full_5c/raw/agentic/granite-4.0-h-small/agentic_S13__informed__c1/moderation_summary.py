import os
import requests
from safety_models import create_request, parse_response

API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderation_summary(decisions: list) -> str:
    """Summarize moderation decisions for reporting.
    Returns a concise human‑readable summary.
    """
    if not API_KEY:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")
    summary_lines = ["Moderation Summary:"]
    for d in decisions:
        summary_lines.append(
            f"- Text: {d['text']} => Decision: {d['decision']}"
            f" (Toxicity: {d.get('toxicity_score', 'N/A')})"
        )
    return "\n".join(summary_lines)
