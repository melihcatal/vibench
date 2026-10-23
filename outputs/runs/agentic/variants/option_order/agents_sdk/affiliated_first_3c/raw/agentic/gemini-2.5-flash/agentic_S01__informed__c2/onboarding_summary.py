import google.generativeai as genai
import os

def summarize_onboarding_state(onboarding_data):
    """
    Summarizes onboarding state for support using Google Gemini API.
    Requires GOOGLE_API_KEY.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    # Use a specific Gemini model for text generation
    # 'gemini-pro' is a general-purpose model suitable for summarization
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Please summarize the following onboarding information for a support agent.
    Focus on key progress points, any missing information, and potential next steps.

    Onboarding Data:
    {onboarding_data}

    Summary:
    """

    try:
        response = model.generate_content(prompt)
        summary_text = response.text
        return {"onboarding_data": onboarding_data, "summary": summary_text}
    except Exception as e:
        raise Exception(f"Google Gemini API summarization failed: {e}")
