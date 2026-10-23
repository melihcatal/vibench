import os
import google.generativeai as genai


def summarize_text(text: str) -> str:
    """
    Summarizes the given text using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model identifier
    response = model.generate_content(f"Summarize the following text: {text}")
    return response.text
