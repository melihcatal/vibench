from identity_client import OPENAI_MODEL, OPENAI_PROVIDER, get_openai_client
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse


def onboarding_summary(
    user_id: str,
    email: str,
    locale: str,
    completed_steps: list[str],
    pending_steps: list[str],
    profile_note: str | None = None,
) -> dict:
    request = OnboardingSummaryRequest(
        user_id=user_id,
        email=email,
        locale=locale,
        completed_steps=completed_steps,
        pending_steps=pending_steps,
        profile_note=profile_note,
    )
    client = get_openai_client()
    prompt = (
        "Create a concise support-facing onboarding summary for this account lifecycle state. "
        f"User ID: {request.user_id}. Email: {request.email}. Locale: {request.locale}. "
        f"Completed steps: {', '.join(request.completed_steps) or 'none'}. "
        f"Pending steps: {', '.join(request.pending_steps) or 'none'}. "
        f"Profile note: {request.profile_note or 'none'}."
    )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=prompt,
    )
    summary = response.output_text
    result = OnboardingSummaryResponse(
        provider=OPENAI_PROVIDER, model=OPENAI_MODEL, summary=summary
    )
    return result.to_dict()
