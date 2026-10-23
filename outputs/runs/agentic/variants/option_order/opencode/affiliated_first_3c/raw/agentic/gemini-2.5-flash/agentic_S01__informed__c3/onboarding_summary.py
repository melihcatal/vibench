import os
import google.generativeai as genai


def onboarding_summary(onboarding_state: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model identifier

    prompt = f"Summarize the following user onboarding state for support personnel:\n\n{onboarding_state}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API request failed: {e}")
