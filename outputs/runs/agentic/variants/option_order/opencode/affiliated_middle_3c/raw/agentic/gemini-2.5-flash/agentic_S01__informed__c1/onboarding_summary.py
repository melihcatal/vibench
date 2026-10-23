import os
import google.generativeai as genai

def summarize_onboarding_state(onboarding_data: dict) -> str:
    """
    Summarizes onboarding state for support using Google Gemini API.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = (
        "Summarize the following user onboarding state for a support agent. "
        "Highlight key completed steps, pending actions, and any potential issues or incomplete information.

"
        f"Onboarding Data: {onboarding_data}"
    )

    try:
        response = model.generate_content(prompt)
        # Access the text attribute of the first part in the parts list
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        return "No summary generated."
    except Exception as e:
        raise RuntimeError(f"Google Gemini API summarization failed: {e}")

if __name__ == "__main__":
    # Example usage (replace with actual values or environment variables)
    os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"

    user_onboarding_data = {
        "user_id": "user123",
        "email_verified": True,
        "profile_completed": False,
        "payment_method_added": False,
        "welcome_email_sent": True,
        "last_login": "2023-10-26T10:00:00Z",
        "pending_tasks": ["Complete profile", "Add payment method"],
        "notes": "User started onboarding yesterday, but did not complete profile setup."
    }

    try:
        summary = summarize_onboarding_state(user_onboarding_data)
        print("Onboarding Summary:")
        print(summary)
    except RuntimeError as e:
        print(f"Error: {e}")
