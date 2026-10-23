import os
import google.generativeai as genai
from model_client import get_gemini_client

def summarize_text(text: str) -> str:
    """
    Calls Google Gemini API to summarize long text.
    """
    client = get_gemini_client()
    model = client.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following text:

{text}"
    response = model.generate_content(prompt)
    return response.text
