import google.generativeai as genai
import os
from typing import Dict

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_message(payload: Dict) -> str:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = f"Summarize the following message payload in one sentence:\n\n{payload}"
    response = model.generate_content(prompt)
    return response.text