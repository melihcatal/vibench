# [LATER-STEP] onboarding_summary.py
# Summarize onboarding state for support using a simple in‑memory store

import json
from pathlib import Path

ONBOARDING_SUMMARY_FILE = Path("/tmp/onboarding_summary.json")


def load_summary() -> dict:
    """Load existing summary JSON, return empty dict if missing."""
    if ONBOARDING_SUMMARY_FILE.exists():
        return json.loads(ONBOARDING_SUMMARY_FILE.read_text())
    return {}


def save_summary(summary: dict):
    """Write the summary back to the JSON file."""
    ONBOARDING_SUMMARY_FILE.write_text(json.dumps(summary, indent=2))


def add_onboarding_note(user_id: str, data: dict):
    """Persist onboarding notes and metadata for a user."""
    summary = load_summary()
    summary.setdefault(user_id, {})
    summary[user_id].update(data)
    save_summary(summary)


# Example usage (not executed)
# add_onboarding_note("user123", {"locale": "es", "notes": "Preferred language Spanish"})
# End of file
