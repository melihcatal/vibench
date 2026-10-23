import os
import google.generativeai as genai


def summarize_meeting_chunk(text_chunk: str) -> str:
    """Summarizes a text chunk using the Google Gemini API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using gemini-pro for text summarization

    prompt = f"Please summarize the following meeting transcript chunk concisely:\n\n{text_chunk}\n\nSummary:"

    response = model.generate_content(prompt)
    return response.text
