import os
import json
from datetime import datetime
from anthropic import Anthropic
from identity_models import OnboardingSummary


ANTHROPIC_MODEL = "claude-3-sonnet-20240229"


def summarize_onboarding_state(
    user_id: str,
    onboarding_data: dict,
    api_key: str = None,
    model: str = ANTHROPIC_MODEL,
) -> OnboardingSummary:
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    system_prompt = (
        "You are a support assistant that summarizes user onboarding state. "
        "Provide a concise, factual summary of the user's onboarding progress, "
        "highlighting completed steps, pending actions, and any issues or flags. "
        "Keep the summary under 150 words."
    )

    user_message = (
        f"Summarize the onboarding state for user {user_id}:\n"
        f"{json.dumps(onboarding_data, indent=2)}"
    )

    message = client.messages.create(
        model=model,
        max_tokens=500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    summary_text = message.content[0].text if message.content else ""

    flags = []
    if onboarding_data.get("email_verified") is False:
        flags.append("email_not_verified")
    if onboarding_data.get("profile_complete") is False:
        flags.append("profile_incomplete")
    if onboarding_data.get("moderation_passed") is False:
        flags.append("moderation_failed")

    return OnboardingSummary(
        user_id=user_id,
        status=onboarding_data.get("status", "in_progress"),
        summary_text=summary_text,
        locale=onboarding_data.get("locale", "en"),
        generated_at=datetime.utcnow().isoformat(),
        flags=flags,
    )


def generate_onboarding_summary_for_support(
    user_id: str,
    registration_date: str = "",
    last_login: str = "",
    steps_completed: list = None,
    steps_pending: list = None,
    issues: list = None,
    locale: str = "en",
    api_key: str = None,
) -> OnboardingSummary:
    onboarding_data = {
        "user_id": user_id,
        "registration_date": registration_date,
        "last_login": last_login,
        "steps_completed": steps_completed or [],
        "steps_pending": steps_pending or [],
        "issues": issues or [],
        "locale": locale,
    }
    return summarize_onboarding_state(user_id, onboarding_data, api_key=api_key)


if __name__ == "__main__":
    result = summarize_onboarding_state(
        user_id="user_12345",
        onboarding_data={
            "email_verified": True,
            "profile_complete": False,
            "moderation_passed": True,
            "status": "in_progress",
            "locale": "en",
        },
    )
    print(result)
