import os
import google.generativeai as genai

def summarize_onboarding_state(user_data: dict, onboarding_steps: list):
    """
    Summarizes the user's onboarding state for support using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        return {"error": "GOOGLE_API_KEY environment variable not set."}

    genai.configure(api_key=google_api_key)

    # Use a specific model that supports text generation, e.g., 'gemini-pro'
    model = genai.GenerativeModel('gemini-pro')

    user_info_str = f"User ID: {user_data.get('uid')}, Email: {user_data.get('email')}, Display Name: {user_data.get('display_name')}"
    onboarding_steps_str = ", ".join(onboarding_steps)

    prompt = f"""
    Summarize the onboarding state for the following user, including completed steps and any pending actions.
    User Information: {user_info_str}
    Completed Onboarding Steps: {onboarding_steps_str}
    """

    try:
        response = model.generate_content(prompt)
        return {"summary": response.text}
    except Exception as e:
        return {"error": f"Error generating summary with Gemini API: {e}"}

