import os
import google.generativeai as genai


def summarize_record(text_content: str) -> str:
    """Summarizes retrieved document records using Google Gemini API.

    Args:
        text_content (str): The text content from the document record to summarize.

    Returns:
        str: The summarized text.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Use a specific model family for text generation
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        f"Please provide a concise summary of the following text:\n\n{text_content}"
    )

    response = model.generate_content(prompt)
    return response.text
