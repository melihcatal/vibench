import google.generativeai as genai
import os

def summarize_onboarding_state(user_id, profile_text, onboarding_steps_completed):
    """
    Summarizes the user's onboarding state for support using Google Gemini API.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        return {"error": "GOOGLE_API_KEY environment variable must be set."}

    genai.configure(api_key=google_api_key)

    try:
        # Using a specific model for text generation
        model = genai.GenerativeModel('gemini-pro')

        prompt = (
            f"Summarize the onboarding state for user '{user_id}'.\n"
            f"Profile text: '{profile_text}'\n"
            f"Completed steps: {', '.join(onboarding_steps_completed) if onboarding_steps_completed else 'None'}.\n"
            "Provide a concise summary suitable for a support agent."
        )

        response = model.generate_content(prompt)
        # Access the text from the first part of the first candidate
        summary = response.candidates[0].content.parts[0].text
        return {"user_id": user_id, "summary": summary}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    test_user_id = "user123"
    test_profile_text = "Enthusiastic new member, loves reading and exploring new tech."
    test_onboarding_steps = ["email_verified", "profile_updated", "first_login"]

    print(f"Summarizing onboarding state for user: {test_user_id}")
    summary_result = summarize_onboarding_state(
        test_user_id,
        test_profile_text,
        test_onboarding_steps
    )
    print(summary_result)
