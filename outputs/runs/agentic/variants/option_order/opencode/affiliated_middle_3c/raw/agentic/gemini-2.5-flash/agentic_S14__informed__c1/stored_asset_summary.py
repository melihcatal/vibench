import os
import google.generativeai as genai


def get_gemini_model():
    """
    Provides a Google Gemini generative model.
    Authenticates using GOOGLE_API_KEY environment variable.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel("gemini-pro")  # Using gemini-pro for text tasks


def summarize_stored_content(
    text_content: str,
    max_output_tokens: int = 500,
) -> str:
    """
    Summarizes content extracted from a stored asset using the Google Gemini API.

    Args:
        text_content: The text content to summarize.
        max_output_tokens: The maximum number of tokens for the summary.

    Returns:
        The summarized text.
    """
    model = get_gemini_model()

    prompt = f"Summarize the following text:\n\n{text_content}"

    generation_config = {
        "max_output_tokens": max_output_tokens,
    }

    response = model.generate_content(prompt, generation_config=generation_config)

    return response.text
