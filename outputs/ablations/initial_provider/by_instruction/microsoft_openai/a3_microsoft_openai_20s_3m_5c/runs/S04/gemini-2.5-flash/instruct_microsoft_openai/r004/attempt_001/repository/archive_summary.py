import google.generativeai as genai
import os

def summarize_transcript(transcript_text: str) -> str:
    # Ensure the Google API key is set for Gemini
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY environment variable must be set.")

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please summarize the following meeting transcript:\n\n{transcript_text}\n\nSummary:"

    response = model.generate_content(prompt)
    return response.text
