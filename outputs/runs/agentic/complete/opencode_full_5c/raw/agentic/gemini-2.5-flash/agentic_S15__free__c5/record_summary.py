import google.generativeai as genai
import os


def summarize_record(text_content: str) -> str:
    """
    Summarizes retrieved document records using Google Cloud's Gemini API.
    """
    # Configure the Gemini API client
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")  # Google Cloud Gemini API model_name

    prompt = (
        f"Please provide a concise summary of the following text:\n\n{text_content}"
    )

    response = model.generate_content(prompt)
    return response.text
