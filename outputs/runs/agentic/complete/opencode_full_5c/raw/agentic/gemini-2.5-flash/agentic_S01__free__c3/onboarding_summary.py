import os
import google.generativeai as genai
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse


def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    # Ensure you have your Google API key set as an environment variable
    # For example: export GOOGLE_API_KEY="YOUR_API_KEY"
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for text generation

    onboarding_data_str = str(request.onboarding_data)
    prompt = f"Summarize the following user onboarding data for a support agent. Highlight key information, potential issues, or areas requiring attention:\n\n{onboarding_data_str}"

    try:
        response = model.generate_content(prompt)
        summary_text = response.text
        return OnboardingSummaryResponse(summary_text=summary_text)
    except Exception as e:
        raise RuntimeError(f"Google Generative AI summarization failed: {e}")


if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY env var)
    os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"

    try:
        sample_onboarding_data = {
            "user_id": "user123",
            "email": "user123@example.com",
            "registration_date": "2023-10-27",
            "last_login": "2023-10-27",
            "profile_completed": True,
            "welcome_email_sent": True,
            "profile_text_moderated": "CLEAN",
            "payment_method_added": False,
            "product_viewed": ["itemA", "itemB"],
            "support_notes": [],
        }
        summary_request = OnboardingSummaryRequest(
            onboarding_data=sample_onboarding_data
        )
        response = onboarding_summary(summary_request)
        print("Onboarding Summary for Support:")
        print(response.summary_text)
    except Exception as e:
        print(f"Error during onboarding summary: {e}")
