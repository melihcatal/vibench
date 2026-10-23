import google.generativeai as genai
import os

def onboarding_summary(onboarding_state: dict) -> str:
    # Ensure GOOGLE_API_KEY env var is set with your Google Cloud API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using Gemini Pro model

    prompt = f"Summarize the following user onboarding state for support personnel, highlighting any pending actions or incomplete steps:\n\n{onboarding_state}"

    response = model.generate_content(prompt)
    return response.text
