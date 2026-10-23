import os
import google.generativeai as genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

genai.configure(api_key=GOOGLE_API_KEY)


def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes a long transcript using the Gemini API.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"Please summarize the following meeting transcript:\n\n{transcript_text}"

    response = model.generate_content(prompt)

    return response.text
