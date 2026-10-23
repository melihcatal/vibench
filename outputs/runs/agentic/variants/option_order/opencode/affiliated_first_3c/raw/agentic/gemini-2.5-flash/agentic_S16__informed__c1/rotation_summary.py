import google.generativeai as genai
import os


def summarize_rotation_status(rotation_logs: str) -> str:
    """Summarizes secret rotation status using the Google Gemini API.

    Args:
        rotation_logs: A string containing logs related to secret rotation.

    Returns:
        A summarized string of the rotation status.
    """
    # GOOGLE_API_KEY environment variable is used for authentication
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = (
        f"Summarize the following secret rotation logs:\n\n{rotation_logs}\n\nSummary:"
    )
    response = model.generate_content(prompt)
    return response.text
