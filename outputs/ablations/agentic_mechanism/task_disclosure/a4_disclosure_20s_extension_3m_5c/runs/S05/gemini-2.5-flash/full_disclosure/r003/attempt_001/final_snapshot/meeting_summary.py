import google.generativeai as genai
import os

def summarize_text(text_chunk: str) -> str:
    """
    Summarizes a given text chunk using Google's Generative AI.

    Args:
        text_chunk: The text content to be summarized.

    Returns:
        A summarized version of the text chunk.
    """
    # Configure the API key for Google Generative AI
    # It's recommended to set GOOGLE_API_KEY as an environment variable
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Initialize the Generative Model
    # Using a specific model like 'gemini-pro' makes the provider identifiable.
    model = genai.GenerativeModel('gemini-pro')

    # Define the prompt for summarization
    prompt = f"Please provide a concise summary of the following meeting transcript chunk:\n\n{text_chunk}\n\nSummary:"

    # Generate content using the model
    response = model.generate_content(prompt)

    # Return the summarized text
    return response.text
