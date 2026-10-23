import os
from typing import Dict, Any
import google.generativeai as genai

def summarize_record(document: Dict[str, Any]) -> str:
    """
    Summarizes a document using Google Gemini API.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    
    text_content = "\n".join(f"{k}: {v}" for k, v in document.items() if isinstance(v, (str, int, float)))
    prompt = f"Summarize the following document in 2-3 sentences:\n\n{text_content}"
    
    response = model.generate_content(prompt)
    return response.text