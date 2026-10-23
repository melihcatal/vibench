import os
import google.generativeai as genai

def summarize_meeting_chunks(transcript_chunks: list[str]):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    full_transcript = " ".join(transcript_chunks)
    prompt = f"Please summarize the following meeting transcript:

{full_transcript}

Summary:"

    response = model.generate_content(prompt)
    return response.text
