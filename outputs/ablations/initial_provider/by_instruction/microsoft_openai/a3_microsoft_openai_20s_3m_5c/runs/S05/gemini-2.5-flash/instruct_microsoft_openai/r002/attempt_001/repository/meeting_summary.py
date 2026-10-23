import google.generativeai as genai
import os

def summarize_meeting_chunks(chunks: list[str]) -> str:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    full_transcript = " ".join(chunks)
    prompt = f"Please summarize the following meeting transcript:\n\n{full_transcript}\n\nSummary:"

    response = model.generate_content(prompt)
    return response.text
