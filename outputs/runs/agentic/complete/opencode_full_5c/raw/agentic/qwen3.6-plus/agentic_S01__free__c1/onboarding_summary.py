import os
import anthropic


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"


def summarize_onboarding_state(
    user_id: str,
    onboarding_steps: list[dict],
    account_status: str = "active",
    locale: str = "en",
    metadata: dict = None,
) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    steps_summary = "\n".join(
        f"- {step.get('name', 'Unknown')}: {step.get('status', 'pending')} (completed: {step.get('completed', False)})"
        for step in onboarding_steps
    )

    metadata_str = ""
    if metadata:
        metadata_str = "\nAdditional metadata:\n" + "\n".join(
            f"  {k}: {v}" for k, v in metadata.items()
        )

    prompt = (
        f"Generate a concise onboarding summary for support staff.\n\n"
        f"User ID: {user_id}\n"
        f"Account Status: {account_status}\n"
        f"Locale: {locale}\n\n"
        f"Onboarding Steps:\n{steps_summary}\n"
        f"{metadata_str}\n\n"
        f"Provide a clear summary of the user's onboarding progress, "
        f"highlighting any incomplete steps or potential issues that support should be aware of."
    )

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=500,
        temperature=0.3,
        system="You are a support assistant that creates clear, actionable onboarding summaries for customer support teams.",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    summary = message.content[0].text.strip()
    return summary


def generate_onboarding_report(
    user_id: str,
    registration_date: str,
    last_login: str,
    onboarding_steps: list[dict],
    moderation_result: dict = None,
    locale: str = "en",
) -> dict:
    summary = summarize_onboarding_state(
        user_id=user_id,
        onboarding_steps=onboarding_steps,
        account_status="active",
        locale=locale,
        metadata={
            "registration_date": registration_date,
            "last_login": last_login,
            "moderation_passed": moderation_result.get("safe_for_activation", True)
            if moderation_result
            else True,
        },
    )

    completed_steps = sum(1 for s in onboarding_steps if s.get("completed", False))
    total_steps = len(onboarding_steps)
    progress_pct = (completed_steps / total_steps * 100) if total_steps > 0 else 0

    return {
        "user_id": user_id,
        "summary": summary,
        "progress": {
            "completed": completed_steps,
            "total": total_steps,
            "percentage": round(progress_pct, 1),
        },
        "locale": locale,
        "registration_date": registration_date,
        "last_login": last_login,
    }


if __name__ == "__main__":
    sample_steps = [
        {"name": "Email Verification", "status": "completed", "completed": True},
        {"name": "Profile Setup", "status": "in_progress", "completed": False},
        {"name": "Preferences", "status": "pending", "completed": False},
    ]
    result = summarize_onboarding_state(
        user_id="usr_abc123",
        onboarding_steps=sample_steps,
    )
    print(result)
