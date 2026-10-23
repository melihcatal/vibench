import os
import google.generativeai as genai

# Google Gemini API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL_NAME = "gemini-pro"

def summarize_meeting_transcript(transcript_chunks: list[str]) -> str:
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    full_transcript = "\n".join(transcript_chunks)

    prompt = f"""Summarize the following meeting transcript. Focus on key decisions, action items, and main discussion points.

Meeting Transcript:
'''
{full_transcript}
'''

Summary:
"""
    response = model.generate_content(prompt)
    return response.text
