import os
import google.generativeai as genai
from model_client import get_gemini_model

def summarize_text(text: str, model_name: str = "gemini-pro") -> str:
    """
    Calls Google Gemini API to summarize long text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = get_gemini_model(model_name)
    prompt = f"Summarize the following text:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text
