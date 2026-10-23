import os
import google.generativeai as genai


def summarize_onboarding_state(onboarding_data: str) -> str:
    """Summarizes onboarding state for support using the Google Gemini API."""
    # Google Gemini API identifies itself via GOOGLE_API_KEY.
    # Ensure GOOGLE_API_KEY environment variable is set.
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")

    genai.configure(api_key=api_key)

    # Using a model from the Gemini family, specifically 'gemini-pro' for text generation
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following onboarding state for a customer support agent:\n\n{onboarding_data}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise ValueError(f"Failed to summarize onboarding state with Gemini API: {e}")
