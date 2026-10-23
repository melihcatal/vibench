from identity_client import openai_client, openai_summary_model
from identity_models import OnboardingSummaryRequest, normalize_openai_summary


def onboarding_summary(request: OnboardingSummaryRequest):
    client = openai_client()
    model = openai_summary_model()
    message = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You summarize onboarding status for support agents in a concise, factual way.",
            },
            {
                "role": "user",
                "content": (
                    f"User ID: {request.user_id}\n"
                    f"Locale: {request.locale or 'unknown'}\n"
                    f"Status: {request.status or 'unknown'}\n"
                    f"Profile text: {request.profile_text}\n"
                    f"Notes: {' | '.join(request.notes) if request.notes else 'none'}\n"
                    "Provide a short support-ready summary with risks or follow-up items if present."
                ),
            },
        ],
    )
    return normalize_openai_summary(message.output_text, model)
