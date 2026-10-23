import google.generativeai as genai
import os
from typing import Dict, Any

def image_summary(analysis_results: Dict[str, Any]) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = "Summarize the following image analysis results in a concise paragraph. " \
             "Focus on key labels, descriptions, detected text, and any safety concerns.\n\n"

    for key, value in analysis_results.items():
        prompt += f"{key}: {value}\n"

    response = model.generate_content(prompt)
    return response.text
