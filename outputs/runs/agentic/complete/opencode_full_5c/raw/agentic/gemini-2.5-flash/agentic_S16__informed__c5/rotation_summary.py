import os
import google.generativeai as genai

def summarize_rotation_status(rotation_logs: str) -> str:
    """Summarizes secret rotation status using the Google Gemini API.

    Args:
        rotation_logs: A string containing the rotation logs or status to summarize.

    Returns:
        A summarized string of the rotation status.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please summarize the following secret rotation status or logs concisely:

{rotation_logs}

Summary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing rotation status: {e}"
