import google.generativeai as genai
import os

def summarize_rotation_status(rotation_log_text: str) -> str | None:
    """
    Summarizes the secret rotation status using the Google Gemini API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY environment variable not set.")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text tasks

    prompt = f"Summarize the following secret rotation status log. Highlight any failures, successes, and next steps:\n\n{rotation_log_text}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing with Gemini API: {e}")
        return None
