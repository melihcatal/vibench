import google.generativeai as genai
import os
from typing import List

def summarize_incident(log_messages: List[str]) -> str:
    """
    Summarize error-log findings for incident review using Google Gemini API.
    """
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = 'Summarize the incident from these error log messages:\\n\\n' + '\\n\\n'.join(log_messages)
    response = model.generate_content(prompt)
    return response.text
