import google.generativeai as genai
from identity_models import OnboardingSummaryPayload
from typing import Dict, Any
import os


def onboarding_summary(payload: OnboardingSummaryPayload, config: Dict[str, Any]) -> Dict[str, str]:
    genai.configure(api_key=config["google_generative_ai_api_key"])
    model = genai.GenerativeModel('gemini-pro')

    onboarding_data_str = str(payload.onboarding_data)

    prompt = f"Summarize the following user onboarding data for a support agent: {onboarding_data_str}"

    response = model.generate_content(prompt)

    return {"summary": response.text}
