import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"

ONBOARDING_STATE_TEMPLATE = """
Summarize the following onboarding state for a support ticket.
Include: user email, registration status, profile completion, moderation status, and any issues.

User Email: {email}
Registration Status: {registration_status}
Profile Completed: {profile_completed}
Moderation Passed: {moderation_passed}
Locale: {locale}
Notes: {notes}
"""


def summarize_onboarding_state(
    email: str,
    registration_status: str,
    profile_completed: bool,
    moderation_passed: bool,
    locale: str = "en",
    notes: str = "",
) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = ONBOARDING_STATE_TEMPLATE.format(
        email=email,
        registration_status=registration_status,
        profile_completed=profile_completed,
        moderation_passed=moderation_passed,
        locale=locale,
        notes=notes,
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a support assistant. Summarize onboarding state concisely "
                    "for internal support tickets. Keep it under 150 words."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    summary = response.choices[0].message.content.strip()
    return summary


def generate_support_summary(onboarding_data: dict) -> str:
    return summarize_onboarding_state(
        email=onboarding_data.get("email", "unknown"),
        registration_status=onboarding_data.get("registration_status", "unknown"),
        profile_completed=onboarding_data.get("profile_completed", False),
        moderation_passed=onboarding_data.get("moderation_passed", False),
        locale=onboarding_data.get("locale", "en"),
        notes=onboarding_data.get("notes", ""),
    )


if __name__ == "__main__":
    sample_data = {
        "email": "user@example.com",
        "registration_status": "completed",
        "profile_completed": True,
        "moderation_passed": True,
        "locale": "en-US",
        "notes": "User signed up via referral link.",
    }
    summary = generate_support_summary(sample_data)
    print(summary)
