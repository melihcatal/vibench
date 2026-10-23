import os
from storage_client import StorageClient


def summarize_content_with_gemini(
    text_content: str, model_name: str = "gemini-pro"
) -> str:
    """Summarizes the provided text content using the Google Gemini API.

    Args:
        text_content (str): The text content to summarize.
        model_name (str): The name of the Gemini model to use (e.g., "gemini-pro").

    Returns:
        str: The summarized text.
    """
    genai = StorageClient.get_generative_model_client()

    model = genai.GenerativeModel(model_name)

    prompt = f"Please summarize the following text: {text_content}"

    print(f"Sending summarization request to Gemini model {model_name}...")
    response = model.generate_content(prompt)

    summary = response.text
    print("Summarization complete.")
    return summary
