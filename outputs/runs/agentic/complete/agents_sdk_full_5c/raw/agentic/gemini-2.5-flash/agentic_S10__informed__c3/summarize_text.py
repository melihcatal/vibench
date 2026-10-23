import os
import google.generativeai as genai
from model_client import get_gemini_model

def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM (Google Gemini) to summarize long text.
    """
    model = get_gemini_model("gemini-pro")
    prompt = f"Summarize the following text:

{text}"
    response = model.generate_content(prompt)
    return response.text
