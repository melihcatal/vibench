from identity_client import openai_request
from identity_models import OnboardingSummaryRequest, normalize_openai_summary


def onboarding_summary(
    user_id: str,
    locale: str,
    steps_completed: list[str],
    profile_text: str | None = None,
    notes: str | None = None,
) -> dict:
    request = OnboardingSummaryRequest(
        user_id=user_id,
        locale=locale,
        steps_completed=steps_completed,
        profile_text=profile_text,
        notes=notes,
    )
    prompt = {
        "user_id": request.user_id,
        "locale": request.locale,
        "steps_completed": request.steps_completed,
        "profile_text": request.profile_text,
        "notes": request.notes,
    }
    response = openai_request(
        "/v1/responses",
        {
            "model": "gpt-4.1-mini",
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Summarize onboarding state for a support agent in a concise paragraph.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": str(prompt)}],
                },
            ],
        },
    )
    summary = normalize_openai_summary(response)
    summary["user_id"] = user_id
    return summary
