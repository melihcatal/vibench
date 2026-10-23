import os
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def summarize_onboarding_state(text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"Summarize the following onboarding state: {text}"
    )
    return response.text
