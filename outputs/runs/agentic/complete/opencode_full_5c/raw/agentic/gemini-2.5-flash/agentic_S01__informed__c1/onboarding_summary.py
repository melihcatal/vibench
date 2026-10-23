import os
import google.generativeai as genai
from typing import Dict, Any

def summarize_onboarding_state(onboarding_data: Dict[str, Any]) -> str:
    """
    Summarizes onboarding state for support using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following user onboarding data for a support agent:

{onboarding_data}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Failed to summarize onboarding state with Gemini API: {e}")