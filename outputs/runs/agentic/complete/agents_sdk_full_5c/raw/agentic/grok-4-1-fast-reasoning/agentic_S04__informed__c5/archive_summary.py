import os
import google.generativeai as genai
from typing import Optional

def archive_summary(transcript: str, max_tokens: int = 500) -> str:
    """
    Summarize transcription results using Google Gemini.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"""
    Provide a concise summary of the following meeting transcript.
    Focus on key points, decisions, and action items.
    Limit to {max_tokens} words.
    
    Transcript:
    {transcript}
    """
    
    response = model.generate_content(prompt)
    return response.text
