import os
import google.generativeai as genai

def summarize_rotation_status(rotation_log_text: str) -> str:
    """
    Summarizes secret rotation status using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Use a specific model, e.g., 'gemini-pro'
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following secret rotation log for an administrator:

{rotation_log_text}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing rotation status with Gemini API: {e}")
        raise
