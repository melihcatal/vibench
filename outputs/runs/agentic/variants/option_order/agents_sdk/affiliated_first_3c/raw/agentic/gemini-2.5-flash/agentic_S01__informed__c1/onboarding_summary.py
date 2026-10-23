import google.generativeai as genai
import os

# Configure the Gemini API client
# Ensure GOOGLE_API_KEY environment variable is set
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_onboarding_state(user_id: str, onboarding_steps: list[str], current_step: str, user_profile_data: dict) -> dict:
    """
    Summarizes onboarding state for support using the Gemini API (gemini-pro model).
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_API_KEY environment variable not set."}

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Summarize the onboarding state for user ID {user_id} for a support agent.

    Onboarding Steps Completed: {", ".join(onboarding_steps)}
    Current Step: {current_step}
    User Profile Data: {user_profile_data}

    Provide a concise summary highlighting:
    - What has been completed.
    - What is the next immediate action for the user or the system.
    - Any potential issues or missing information based on the profile data.
    """

    try:
        response = model.generate_content(prompt)
        # Assuming the response text is the summary
        return {
            "user_id": user_id,
            "summary": response.text,
            "message": "Onboarding state summarized successfully."
        }
    except Exception as e:
        return {"error": str(e)}
