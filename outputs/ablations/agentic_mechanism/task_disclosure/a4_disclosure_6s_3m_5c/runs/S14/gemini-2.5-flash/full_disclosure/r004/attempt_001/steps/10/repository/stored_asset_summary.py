import google.generativeai as genai
import os

def summarize_asset_content(text_content: str) -> str:
    """
    Summarizes content extracted from a stored asset using Google's Generative AI.

    Args:
        text_content: The text content to be summarized.

    Returns:
        A summarized version of the text content.
    """
    # Configure the API key. It's recommended to set this as an environment variable.
    # For demonstration purposes, we are using os.getenv.
    # In a production environment, consider more secure ways to manage API keys.
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Initialize the Generative Model
    # Using a common Gemini model suitable for text generation and summarization
    model = genai.GenerativeModel('gemini-pro')

    # Create the prompt for summarization
    prompt = f"Please provide a concise summary of the following text:

{text_content}"

    # Generate content (summary)
    response = model.generate_content(prompt)

    # Return the summarized text
    return response.text.strip()
