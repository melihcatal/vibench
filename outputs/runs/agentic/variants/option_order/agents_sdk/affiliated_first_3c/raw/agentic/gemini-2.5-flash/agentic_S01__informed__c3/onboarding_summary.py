import google.generativeai as genai
import os

def summarize_onboarding_state(onboarding_data: dict) -> str:
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    genai.configure(api_key=google_api_key)

    # Using a specific model, e.g., 'gemini-pro'
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following user onboarding state for support personnel, highlighting any incomplete steps or unusual data:\n\n{onboarding_data}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Failed to summarize onboarding state: {e}")
