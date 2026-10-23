import google.generativeai as genai
import os

def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM (Google Gemini) to summarize long text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following text:

{text}"
    response = model.generate_content(prompt)
    return response.text
