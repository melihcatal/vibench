import os
import google.generativeai as genai

def summarize_transcript(transcript_text: str):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"Summarize the following transcript:

{transcript_text}"
    response = model.generate_content(prompt)
    
    return response.text
