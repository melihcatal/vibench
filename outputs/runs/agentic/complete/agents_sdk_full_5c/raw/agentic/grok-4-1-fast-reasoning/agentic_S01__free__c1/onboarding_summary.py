import os
import google.generativeai as genai
from typing import Any

def summarize_onboarding_state(onboarding_data: dict[str, Any]) -> str:
    api_key = os.environ["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Summarize the following onboarding state for support team:\n{onboarding_data}"
    response = model.generate_content(prompt)
    return response.text