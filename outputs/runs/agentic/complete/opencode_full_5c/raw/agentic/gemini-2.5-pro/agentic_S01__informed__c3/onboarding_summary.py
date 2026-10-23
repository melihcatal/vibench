import os
import google.generativeai as genai
from identity_models import OnboardingState


def summarize_onboarding(state: OnboardingState) -> str:
    """
    Summarizes a user's onboarding state for support tickets using the Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Summarize the onboarding state for user {state.user_id}.
    This summary is for an internal support agent.
    
    User Locale: {state.user_locale}
    Profile Text: "{state.profile_text}"
    
    Moderation Results (0=Safe, higher=severe):
    {state.moderation_result}
    
    Translation of welcome message:
    {state.translation_result}

    Provide a brief, one-paragraph summary.
    """

    response = model.generate_content(prompt)

    return response.text
