import os
import openai
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse

def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    onboarding_steps_text = ", ".join(request.onboarding_steps)

    try:
        # Using a chat model to summarize onboarding state
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Concrete model identifier
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes user onboarding states."},
                {"role": "user", "content": f"Summarize the onboarding steps for user {request.user_id}: {onboarding_steps_text}. Provide a concise summary for a support agent."}
            ]
        )
        summary_text = response.choices[0].message.content.strip()
    except Exception as e:
        summary_text = f"Failed to generate summary: {e}"

    return OnboardingSummaryResponse(
        summary=summary_text
    )
