import os
import google.generativeai as genai


def summarize_message(content: str) -> str:
    """Summarizes message content using the Google Gemini API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following message content in one sentence:\n\n{content}"

    response = model.generate_content(prompt)

    return response.text
