import google.generativeai as genai
import os


def summarize_transcript(transcript_text: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Please provide a concise summary of the following transcript:\n\n{transcript_text}\n\nSummary:"
    response = model.generate_content(prompt)
    return response.text
