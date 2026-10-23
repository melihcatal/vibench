import google.generativeai as genai
import os

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def onboarding_summary(onboarding_state: dict):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following user onboarding state for a support agent: {onboarding_state}"
    response = model.generate_content(prompt)
    return response.text
