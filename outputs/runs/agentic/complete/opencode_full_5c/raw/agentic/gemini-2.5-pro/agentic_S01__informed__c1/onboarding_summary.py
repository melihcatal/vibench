import os
import google.generativeai as genai


def summarize_onboarding_state(onboarding_data: dict) -> str:
    """
    Summarizes the user's onboarding state for support using Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Summarize the following user onboarding data for a support ticket.
    Highlight any potential issues or incomplete steps.

    Data:
    ---
    {onboarding_data}
    ---

    Summary:
    """

    response = model.generate_content(prompt)
    return response.text
