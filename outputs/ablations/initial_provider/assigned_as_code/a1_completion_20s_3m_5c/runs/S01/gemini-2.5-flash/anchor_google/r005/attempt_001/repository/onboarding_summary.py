import google.generativeai as genai
import os
from identity_models import OnboardingSummaryPayload

def onboarding_summary(payload: OnboardingSummaryPayload):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following onboarding data for user ID {payload.user_id}:\n{payload.onboarding_data}"
    
    response = model.generate_content(prompt)
    
    return {
        "summary": response.text,
        "model": "gemini-pro",
        "provider": "Google Cloud Generative AI"
    }
