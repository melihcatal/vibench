import google.generativeai as genai
import os
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse


def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Use a specific Gemini model for text generation tasks
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following onboarding data in a concise manner for a support agent: {request.onboarding_data}"

    try:
        response = model.generate_content(prompt)
        return OnboardingSummaryResponse(summary=response.text)
    except Exception as e:
        raise ValueError(f"Google Gemini API summary failed: {e}")
