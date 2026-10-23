import google.generativeai as genai
import os

def summarize_onboarding_state(onboarding_data: str) -> str:
    # Configure Google Generative AI with an API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)

    # Use a specific model, e.g., "gemini-pro"
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following user onboarding state for a support agent:

{onboarding_data}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Failed to summarize onboarding state with Gemini API: {e}")
