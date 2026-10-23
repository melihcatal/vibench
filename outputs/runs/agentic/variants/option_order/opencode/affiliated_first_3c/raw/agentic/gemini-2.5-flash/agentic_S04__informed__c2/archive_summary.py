import os
import google.generativeai as genai

def summarize_transcript(transcript_text: str) -> str:
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Use the Gemini Pro model for text generation
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following meeting transcript:
\n{transcript_text}\n\nSummary:"

    response = model.generate_content(prompt)
    return response.text
