import os
import google.generativeai as genai

def summarize_meeting_chunks(transcript_chunks):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    full_transcript = " ".join(transcript_chunks)
    prompt = f"Summarize the following meeting transcript:

{full_transcript}"

    response = model.generate_content(prompt)
    return response.text