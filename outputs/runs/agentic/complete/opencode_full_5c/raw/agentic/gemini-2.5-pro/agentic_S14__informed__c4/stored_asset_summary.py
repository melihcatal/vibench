import os
import google.generativeai as genai


def summarize_text_with_gemini(text: str) -> str:
    """
    Summarizes the given text using the Google Gemini API.

    Args:
        text: The text to be summarized.

    Returns:
        The summarized text as a string.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    prompt = f"Please summarize the following text:\n\n{text}"

    response = model.generate_content(prompt)

    return response.text
