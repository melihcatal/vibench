import google.generativeai as genai
import os

def summarize_meeting_transcript(transcript_chunk: str) -> str:
    """Summarizes live meeting transcript chunks using the Google Gemini API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please summarize the following meeting transcript chunk:

{transcript_chunk}\nSummary:"

    response = model.generate_content(prompt)
    return response.text
