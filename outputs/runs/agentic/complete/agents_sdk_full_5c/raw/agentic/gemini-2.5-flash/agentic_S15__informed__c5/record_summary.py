import os
import google.generativeai as genai

def record_summary(document_content: str) -> str:
    """
    Summarize retrieved document records using Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"Please provide a concise summary of the following document content:

{document_content}"

    response = model.generate_content(prompt)
    return response.text
