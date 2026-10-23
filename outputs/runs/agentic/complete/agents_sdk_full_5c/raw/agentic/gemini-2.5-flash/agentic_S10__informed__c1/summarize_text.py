import os
import google.generativeai as genai
from model_client import get_gemini_model

def summarize_text(text: str, model_name: str = "gemini-pro") -> str:
    """
    Calls Google Gemini API to summarize long text.
    """
    model = get_gemini_model(model_name)
    prompt = f"Summarize the following text:

{text}"
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY env var)
    # print(summarize_text("The quick brown fox jumps over the lazy dog. This is a simple sentence for testing purposes."))
    pass
