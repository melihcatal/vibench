import os
import json
from typing import TypedDict
import requests


class OnboardingResponse(TypedDict):
    user_id: str
    steps_completed: int
    notes: Optional[str]


def summarize_onboarding(
    user_id: str, api_endpoint: str, api_key: str
) -> OnboardingResponse:
    """Summarize onboarding state for support.

    In a full implementation this would call a monitoring or logging service.
    Returns a simple JSON-like dict summarizing what we know.
    """
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        resp = requests.get(
            f"{api_endpoint}/users/{user_id}/onboarding", headers=headers, timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        # Extract a few key fields for a quick support snapshot
        return OnboardingResponse(
            user_id=user_id,
            steps_completed=data.get("steps_completed", 0),
            notes=data.get("notes", ""),
        )
    except requests.RequestException as e:
        raise RuntimeError(f"Onboarding summary fetch failed: {e}")
