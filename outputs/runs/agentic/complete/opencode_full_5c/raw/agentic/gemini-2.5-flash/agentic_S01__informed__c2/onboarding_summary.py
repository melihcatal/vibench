from identity_client import GoogleGeminiClient
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse


def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    client = GoogleGeminiClient()
    # For a real application, you might use a more sophisticated prompt or a specific model fine-tuned for summarization.
    prompt = f"Summarize the following onboarding data for support purposes: {request.onboarding_data}"
    response = client.model.generate_content(prompt)
    return OnboardingSummaryResponse(summary=response.text)
