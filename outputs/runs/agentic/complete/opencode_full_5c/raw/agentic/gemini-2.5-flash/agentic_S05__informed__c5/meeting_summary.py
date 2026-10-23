import os
import google.generativeai as genai

def summarize_meeting_chunk(text_chunk: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following meeting transcript chunk concisely:

{text_chunk}"
    response = model.generate_content(prompt)
    return response.text
