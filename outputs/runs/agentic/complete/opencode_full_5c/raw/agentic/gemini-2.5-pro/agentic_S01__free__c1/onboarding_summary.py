import os
import google.generativeai as genai
from identity_models import ProfileData


def summarize_onboarding(profile_data: ProfileData) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY environment variable not set."}

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Summarize the onboarding status for a new user for our support team.
    User ID: {profile_data.user_id}
    Profile Text: "{profile_data.profile_text}"
    Internal Notes: {profile_data.notes}

    Provide a concise summary of any potential issues or next steps.
    """

    try:
        response = model.generate_content(prompt)
        return {"summary": response.text}
    except Exception as e:
        return {"error": str(e)}
