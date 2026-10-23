# [LATER-STEP] onboarding_summary.py
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse
from typing import Dict

# Placeholder for an LLM or summarization service (e.g., OpenAI, Claude)


def generate_onboarding_summary(request: OnboardingSummaryRequest) -> str:
    # Simulated summary: in production replace with LLM call
    user_id = request.user_id
    summary = (
        f"User {user_id} has completed basic profile setup. \n"
        "Next steps: verify email, set preferences, and connect social accounts."
    )
    return summary


def summarize_onboarding_state(
    request: OnboardingSummaryRequest,
) -> OnboardingSummaryResponse:
    summary_text = generate_onboarding_summary(request)
    return OnboardingSummaryResponse(summary=summary_text)
