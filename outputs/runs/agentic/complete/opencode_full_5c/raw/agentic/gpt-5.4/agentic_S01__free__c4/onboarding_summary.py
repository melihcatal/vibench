from __future__ import annotations

import requests

from identity_client import OPENAI_RESPONSES_URL, openai_headers, openai_model
from identity_models import SummaryResult


def onboarding_summary(onboarding_state: dict):
    prompt = (
        "Summarize this user onboarding state for a support agent in under 120 words. "
        "Highlight blockers, verification progress, and next actions.\n\n"
        f"State: {onboarding_state}"
    )
    payload = {
        "model": openai_model(),
        "input": prompt,
    }
    response = requests.post(
        OPENAI_RESPONSES_URL, headers=openai_headers(), json=payload, timeout=30
    )
    response.raise_for_status()
    data = response.json()
    summary = data.get("output_text", "")
    return SummaryResult(provider="openai", summary=summary, model=payload["model"])
