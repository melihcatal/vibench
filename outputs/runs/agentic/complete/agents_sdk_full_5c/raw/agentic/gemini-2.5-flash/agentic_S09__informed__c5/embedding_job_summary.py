import os
import google.generativeai as genai

def summarize_embedding_results(text_results: str) -> str:
    """Summarizes embedding job results using Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the following text about embedding job results:

{text_results}

Summary:"""

    response = model.generate_content(prompt)
    return response.text

