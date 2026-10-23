import os
import google.generativeai as genai


def summarize_onboarding_data(onboarding_data: dict) -> str:
    """
    Summarizes the user's onboarding state for a support ticket
    using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Summarize the following user onboarding data into a brief note for a support agent.
    Focus on any potential issues or incomplete steps.

    Data:
    ---
    Email Verified: {onboarding_data.get("email_verified")}
    Profile Complete: {onboarding_data.get("profile_complete")}
    Last Login: {onboarding_data.get("last_login")}
    Profile Moderation Flags: {onboarding_data.get("moderation_flags")}
    ---
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"
