import google.generativeai as genai
import os

def onboarding_summary(onboarding_state: dict) -> dict:
    # Configure the Google Gemini API key
    # Requires GOOGLE_API_KEY to be set in environment variables
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY must be set in environment variables.")
    genai.configure(api_key=google_api_key)

    # Choose a model, e.g., 'gemini-pro'
    # For text generation, 'gemini-pro' is a good general-purpose model.
    model = genai.GenerativeModel('gemini-pro')

    # Craft a prompt for summarizing the onboarding state
    prompt = f"Summarize the following user onboarding state for a support agent. Highlight any incomplete steps or potential issues:\n\n{onboarding_state}"

    try:
        response = model.generate_content(prompt)
        summary_text = response.text
        return {"onboarding_summary": summary_text}
    except Exception as e:
        raise RuntimeError(f"Failed to generate onboarding summary with Gemini API: {e}")

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY to be set)
    # import os
    # os.environ['GOOGLE_API_KEY'] = "YOUR_GOOGLE_API_KEY"
    # try:
    #     user_onboarding_data = {
    #         "user_id": "user123",
    #         "email_verified": True,
    #         "profile_complete": False,
    #         "payment_method_added": False,
    #         "welcome_email_sent": True,
    #         "last_login": "2023-10-26T10:00:00Z"
    #     }
    #     summary = onboarding_summary(user_onboarding_data)
    #     print(f"Onboarding Summary: {summary}")
    #
    #     user_onboarding_complete = {
    #         "user_id": "user456",
    #         "email_verified": True,
    #         "profile_complete": True,
    #         "payment_method_added": True,
    #         "welcome_email_sent": True,
    #         "last_login": "2023-10-25T15:30:00Z"
    #     }
    #     summary_complete = onboarding_summary(user_onboarding_complete)
    #     print(f"Complete Onboarding Summary: {summary_complete}")
    #
    # except RuntimeError as e:
    #     print(f"Error during summary generation: {e}")
    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    pass
