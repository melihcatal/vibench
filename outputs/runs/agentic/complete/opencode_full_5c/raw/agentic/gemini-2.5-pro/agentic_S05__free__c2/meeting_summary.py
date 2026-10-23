import os
import google.generativeai as genai


def summarize_meeting_transcript(transcript_chunks):
    """Summarizes live meeting transcript chunks."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable must be set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    full_transcript = " ".join(transcript_chunks)
    prompt = f"Please summarize the following meeting transcript:\n\n{full_transcript}"

    response = model.generate_content(prompt)

    return response.text
