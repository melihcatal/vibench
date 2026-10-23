import os
import google.generativeai as genai

def summarize_transcription_results(transcript_text: str) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"Summarize the following meeting transcript:

{transcript_text}

Summary:"

    response = model.generate_content(prompt)
    return response.text
