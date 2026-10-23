import os

import google.generativeai as genai

from identity_models import OnboardingSummaryRequest

def onboarding_summary(payload: OnboardingSummaryRequest, config: Optional[Dict[str, Any]] = None):
    # Ensure GOOGLE_API_KEY environment variable is set for authentication
    # or provide credentials via config.
    
    api_key = config.get("google_api_key", os.environ.get("GOOGLE_API_KEY"))
    if not api_key:
        raise ValueError("Google API Key must be provided in config or environment variable GOOGLE_API_KEY.")
    
    genai.configure(api_key=api_key)

    # Using a generative model like Gemini for summarization
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text tasks

    onboarding_data_str = "\n".join([f"{k}: {v}" for k, v in payload.onboarding_data.items()])
    prompt = f"Summarize the following onboarding information for user {payload.user_id}:\n\n{onboarding_data_str}\n\nProvide a concise summary highlighting key steps completed and any outstanding items."

    response = model.generate_content(prompt)
    
    summary_text = response.text

    return {
        "user_id": payload.user_id,
        "onboarding_data": payload.onboarding_data,
        "summary": summary_text
    }
