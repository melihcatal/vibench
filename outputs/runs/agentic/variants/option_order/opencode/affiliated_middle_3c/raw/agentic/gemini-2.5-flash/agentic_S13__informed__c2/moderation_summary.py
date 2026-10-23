import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_moderation_decisions(decisions: List[Dict[str, Any]]) -> str:
    """
    Summarize moderation decisions using Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following moderation decisions. Highlight the key reasons for any 'not allowed' decisions:

"
    for decision in decisions:
        prompt += f"Text: {decision['text']}, Decisions: {decision['decisions']}\n"

    response = model.generate_content(prompt)
    return response.text
