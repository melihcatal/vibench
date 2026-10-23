# LATER-STEP: Summarize moderation decisions

from safety_client import get_client
from safety_models import ModerationResult

STATUS_LABELS = {
    "allowed": "Approved",
    "flagged": "Blocked",
    "needs_review": "Pending Review",
}


def summarize_decision(text: str, result: ModerationResult) -> dict:
    """Return a short summary for reporting systems."""
    status = "flagged" if result["flagged"] else "allowed"
    summary = {
        "text": text,
        "status": status,
        "label": STATUS_LABELS[status],
        "categories": result["categories"],
    }
    return summary
