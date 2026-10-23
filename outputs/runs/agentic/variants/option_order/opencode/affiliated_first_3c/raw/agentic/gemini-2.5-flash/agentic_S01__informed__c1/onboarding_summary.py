import google.generativeai as genai
import os

# Configure the Gemini API client
# Ensure GOOGLE_API_KEY is set in your environment variables.
# For example: export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")


def summarize_onboarding_state(onboarding_data: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = (
            f"Summarize the following onboarding state for a support agent. "
            f"Highlight key progress, any pending steps, and potential issues:\n\n{onboarding_data}"
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Gemini API summarization failed: {e}")
