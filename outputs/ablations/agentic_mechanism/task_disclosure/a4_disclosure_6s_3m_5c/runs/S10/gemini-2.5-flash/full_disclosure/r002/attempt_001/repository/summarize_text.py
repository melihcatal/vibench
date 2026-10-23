import google.generativeai as genai
import os

def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM to summarize long text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Summarize the following text:

{text}")
    return response.text
