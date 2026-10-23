import json
from typing import Dict, Any


def onboarding_summary(user_id: str, activity_log: Dict[str, Any]) -> str:
    """Create a concise onboarding state summary for support staff.

    Aggregates key events from activity_log (e.g., registration timestamp,
    welcome email sent, profile approval status). Returns a human‑readable
    summary string.
    """
    summary_parts = []
    summary_parts.append(f"User ID: {user_id}")
    summary_parts.append(
        f"Registration Time (UTC): {activity_log.get('registered_at')}"
    )
    summary_parts.append(f"Locale: {activity_log.get('locale')}")
    summary_parts.append(
        f"Profile Approved: {activity_log.get('profile_approved', False)}"
    )
    summary_parts.append(
        f"Welcome Email Sent: {activity_log.get('welcome_email_sent', False)}"
    )
    # Add any additional notes that were persisted
    notes = activity_log.get("notes")
    if notes:
        summary_parts.append(f"Support Notes: {notes}")
    return "\n".join(summary_parts)
