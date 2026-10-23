import os
import google.generativeai as genai
from typing import Dict, Any


def image_summary(analysis: Dict[str, Any]) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Summarize the visual analysis results:\\n{analysis}"
    response = model.generate_content(prompt)
    return response.text
