import os
import google.generativeai as genai

def summarize_stored_asset(text: str) -> str:
    """Summarizes content extracted from a stored asset using Google Cloud Generative AI (Gemini Pro).

    Args:
        text: The text content to summarize.

    Returns:
        A summarized version of the text.
    """
    # Ensure GOOGLE_API_KEY environment variable is set for authentication
    # os.environ['GOOGLE_API_KEY'] = "YOUR_API_KEY"

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for summarization

    prompt = f"Please summarize the following text:

{text}"

    response = model.generate_content(prompt)
    return response.text
