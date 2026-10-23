import os
import requests
from identity_models import SummaryRequest, SummaryResponse


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"


def summarize_onboarding(
    onboarding_data: dict,
    model: str = ANTHROPIC_MODEL,
) -> SummaryResponse:
    request = SummaryRequest(onboarding_data=onboarding_data, model=model)
    messages = request.to_anthropic_messages()

    payload = {
        "model": model,
        "max_tokens": 1024,
        "messages": messages,
        "system": (
            "You are a helpful assistant that summarizes user onboarding state for support agents. "
            "Keep the summary concise and actionable."
        ),
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
    }

    resp = requests.post(ANTHROPIC_API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    return SummaryResponse.from_anthropic_response(data)


if __name__ == "__main__":
    sample_data = {
        "user_id": "auth0|123456",
        "email": "user@example.com",
        "locale": "es",
        "account_status": "pending_activation",
        "moderation_passed": True,
        "welcome_translated": True,
    }
    result = summarize_onboarding(onboarding_data=sample_data)
    print(result)
