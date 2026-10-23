import os
import google.generativeai as genai
from identity_models import OnboardingSummary

def onboarding_summary(payload, config=None) -> OnboardingSummary:
    config = config or {}
    # Ensure GOOGLE_API_KEY environment variable is set or passed in config
    api_key = config.get("google_api_key", os.environ.get("GOOGLE_API_KEY"))
    if not api_key:
        raise ValueError("Google API Key must be provided in config or GOOGLE_API_KEY environment variable.")

    genai.configure(api_key=api_key)

    model_name = config.get("gemini_model", "gemini-pro") # Using gemini-pro for text tasks
    model = genai.GenerativeModel(model_name)

    onboarding_data = payload["onboarding_data"]
    user_id = payload["user_id"]
    
    prompt = f"Summarize the following user onboarding data: {onboarding_data}\n\nProvide a concise summary of the user's onboarding status and any key information. Keep it under 100 words."

    response = model.generate_content(prompt)
    summary_text = response.text
    
    # Determine status based on summary content or other payload info
    # This is a placeholder; real logic would analyze the data more deeply.
    status = "onboarding_in_progress"
    if "completed" in summary_text.lower():
        status = "onboarding_completed"
    elif "pending" in summary_text.lower():
        status = "onboarding_pending"

    return OnboardingSummary(
        user_id=user_id,
        summary_text=summary_text,
        status=status
    )
