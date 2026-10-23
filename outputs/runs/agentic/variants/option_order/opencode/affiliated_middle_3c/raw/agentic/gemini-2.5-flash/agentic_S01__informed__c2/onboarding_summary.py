import os
import google.generativeai as genai
from identity_models import SummaryRequest, SummaryResponse


def onboarding_summary(request: SummaryRequest) -> SummaryResponse:
    # Gemini API: service=Google Gemini API; sdk=google-genai; interface=sdk; auth=GOOGLE_API_KEY
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Use a specific Gemini model for text generation
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following onboarding state for support: {request.text}"
    response = model.generate_content(prompt)

    return SummaryResponse(summary=response.text)
