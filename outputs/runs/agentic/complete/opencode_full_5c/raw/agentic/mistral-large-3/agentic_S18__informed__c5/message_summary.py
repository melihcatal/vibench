import google.generativeai as genai
import os
from typing import Dict, Any

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def message_summary(message: Dict[str, Any]) -> str:
    prompt = f"Summarize the following message in 2-3 sentences: {message}"
    response = model.generate_content(prompt)
    return response.text
