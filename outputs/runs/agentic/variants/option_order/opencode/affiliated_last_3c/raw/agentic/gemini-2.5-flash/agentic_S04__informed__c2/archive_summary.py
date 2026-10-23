import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_transcript(transcript_text: str) -> str:
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following transcript:

{transcript_text}"
    response = model.generate_content(prompt)
    return response.text
