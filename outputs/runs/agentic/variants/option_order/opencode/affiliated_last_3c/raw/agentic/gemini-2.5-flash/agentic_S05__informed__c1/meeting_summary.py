import os
import google.generativeai as genai

# GOOGLE_API_KEY environment variable should be set
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


def summarize_meeting_chunks(transcript_chunks: list[str]) -> str:
    """Summarizes live meeting transcript chunks using the Google Gemini API."""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for summarization

    full_transcript = "\n".join(transcript_chunks)

    prompt = f"""Summarize the following meeting transcript:

{full_transcript}

Summary:"""

    response = model.generate_content(prompt)
    return response.text
