import os
import google.generativeai as genai


def rotation_summary(rotation_notes: str) -> str:
    """Summarizes secret rotation status using Google Gemini API.

    Args:
        rotation_notes: A string containing notes about secret rotation status.

    Returns:
        A summarized string of the rotation notes.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following secret rotation notes:\n\n{rotation_notes}"
    response = model.generate_content(prompt)
    return response.text
