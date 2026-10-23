import google.generativeai as genai
import os

def summarize_message(text: str) -> str:
    # Provider: Google Gemini API
    # Model: gemini-pro
    # Auth: GOOGLE_API_KEY
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Please provide a concise summary of the following text:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text
