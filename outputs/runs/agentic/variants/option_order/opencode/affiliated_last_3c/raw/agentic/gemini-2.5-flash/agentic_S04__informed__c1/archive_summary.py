import google.generativeai as genai
import os
from typing import Dict, Any

def summarize_transcript(transcript_text: str) -> Dict[str, Any]:
    """
    Summarizes transcription results using the Google Gemini API.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following meeting transcript:

{transcript_text}

Summary:"
    response = model.generate_content(prompt)
    
    return {"summary": response.text}
