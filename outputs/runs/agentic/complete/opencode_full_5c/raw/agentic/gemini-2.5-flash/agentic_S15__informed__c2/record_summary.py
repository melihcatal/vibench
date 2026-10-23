import os
import google.generativeai as genai
from typing import Dict, Any

def summarize_document(document_text: str) -> Dict[str, Any]:
    """
    Summarizes retrieved document records using Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following document:

{document_text}"
    response = model.generate_content(prompt)
    return {"summary": response.text}
