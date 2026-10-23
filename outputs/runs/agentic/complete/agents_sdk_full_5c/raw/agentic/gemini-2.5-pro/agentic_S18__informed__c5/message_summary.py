import os
import google.generativeai as genai

def summarize_text(text_content: str) -> str:
    """
    Summarizes the provided text using the Google Gemini API.

    Args:
        text_content: The text to be summarized.

    Returns:
        The summarized text.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"Please provide a concise, one-sentence summary of the following text:\n\n{text_content}"
    
    response = model.generate_content(prompt)
    
    return response.text.strip()
