import google.generativeai as genai
import json
import os

from identity_client import GoogleCloudConfig
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse

# Configure Generative AI client
if GoogleCloudConfig.API_KEY:
    genai.configure(api_key=GoogleCloudConfig.API_KEY)


def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    """
    Summarizes onboarding state for support using Google Cloud Generative AI.
    """
    model = genai.GenerativeModel("gemini-pro")

    onboarding_data_str = json.dumps(request.onboarding_data, indent=2)

    prompt = f"""Summarize the following onboarding state for user ID {request.user_id}. Highlight key milestones, incomplete steps, or any unusual data points for support personnel:

{onboarding_data_str}

Summary:"""

    try:
        response = model.generate_content(prompt)

        summary_text = ""
        if (
            response.candidates
            and response.candidates[0].content
            and response.candidates[0].content.parts
        ):
            summary_text = response.candidates[0].content.parts[0].text

        return OnboardingSummaryResponse(summary_text=summary_text)

    except Exception as e:
        raise ValueError(f"Failed to summarize onboarding state: {e}")
