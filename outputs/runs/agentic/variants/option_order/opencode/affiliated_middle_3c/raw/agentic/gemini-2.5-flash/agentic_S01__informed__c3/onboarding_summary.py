import os
import google.generativeai as genai
from identity_models import SummarizeOnboardingRequest, SummarizeOnboardingResponse


def onboarding_summary(
    request: SummarizeOnboardingRequest,
) -> SummarizeOnboardingResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Use a specific Gemini model for text generation
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following onboarding data: {request.onboarding_data}"
    response = model.generate_content(prompt)

    summary_text = response.text

    return SummarizeOnboardingResponse(summary=summary_text)
