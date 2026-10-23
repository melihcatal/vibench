from __future__ import annotations

from identity_client import get_openai_headers, post_json
from identity_models import OnboardingSummaryRequest


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_SUMMARY_MODEL = "gpt-4.1-mini"


def onboarding_summary(request: OnboardingSummaryRequest):
    prompt = (
        "Summarize this customer onboarding state for a support agent in under 120 words. "
        "Highlight blockers, verification status, and next best action.\n\n"
        f"Onboarding state: {request.onboarding_state}"
    )
    response = post_json(
        OPENAI_RESPONSES_URL,
        get_openai_headers(),
        {
            "model": OPENAI_SUMMARY_MODEL,
            "input": prompt,
        },
    )
    text = response.get("output", [])[0].get("content", [])[0].get("text", "")
    return {
        "summary": text,
        "provider": "openai",
        "model": OPENAI_SUMMARY_MODEL,
    }
