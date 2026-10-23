import os
import google.generativeai as genai
from model_client import get_gemini_model

def extract_json(text: str) -> str:
    """
    Calls a hosted LLM (Google Gemini) to extract structured JSON from text.
    """
    model = get_gemini_model("gemini-pro")
    prompt = f"""Extract structured JSON from the following text. The JSON should represent key information.
Ensure the output is valid JSON and nothing else.

Text:
{text}

JSON:
"""
    response = model.generate_content(prompt)
    return response.text
