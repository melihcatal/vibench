import google.genai
from model_client import get_model_client


def summarize_text(prompt, max_output_tokens=200):
    """Summarizes long text using Google Gemini API.

    Args:
        prompt (str): The text to summarize.
        max_output_tokens (int): Maximum tokens for the summary.

    Returns:
        str: The summarized text.
    """
    client = get_model_client("gemini")
    response = client.generate_content(
        prompt,
        generation_params={
            "temperature": 0.7,
            "max_output_tokens": max_output_tokens,
            "response_mime_type": "text/plain",
        },
    )
    return response.text
