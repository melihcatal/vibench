import google.generativeai as genai
import os

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def summarize_meeting_chunks(chunks: list[str]):
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    full_transcript = " ".join(chunks)
    prompt = f"Summarize the following meeting transcript:

{full_transcript}"

    response = model.generate_content(prompt)
    return response.text
