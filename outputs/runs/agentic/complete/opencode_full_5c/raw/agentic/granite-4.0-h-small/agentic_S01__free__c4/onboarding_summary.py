import os
import json


def onboarding_summary(metadata: dict) -> str:
    """Summarize onboarding state for support.

    This helper aggregates essential fields from the onboarding payload.

    No external provider is used; purely local summarization logic.
    """
    summary_lines = []
    summary_lines.append(f"UserID: {metadata.get('user_id', 'N/A')}")
    summary_lines.append(f"Email: {metadata.get('email', 'N/A')}")
    summary_lines.append(f"Locale: {metadata.get('locale', 'N/A')}")
    summary_lines.append(
        f"Profile Moderation Status: {'CLEAN' if metadata.get('moderation_status') == 'clean' else 'ISSUES'}"
    )
    summary_lines.append(
        f"Onboarding Completed: {metadata.get('completed_at', 'Pending')}"
    )
    return "\n".join(summary_lines)
