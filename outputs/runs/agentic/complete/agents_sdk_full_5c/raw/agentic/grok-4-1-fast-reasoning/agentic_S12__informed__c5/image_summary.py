import os
import json
import google.generativeai as genai
from typing import Dict, Any

def image_summary(analysis_results: Dict[str, Any]) -> str:
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        "Provide a concise summary of the image based on the following analysis results:\n\n"
        + json.dumps(analysis_results, indent=2)
    )
    response = model.generate_content(prompt)
    return response.text