import os
import google.generativeai as genai

def summarize_meeting_chunks(text_chunks: list[str]) -> str:
    """
    Summarizes live meeting transcript chunks using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Provider-identifying signal: google.generativeai and model ID
    model = genai.GenerativeModel('gemini-pro')

    full_transcript = " ".join(text_chunks)

    prompt = f"Please provide a concise summary of the following meeting transcript:
\n{full_transcript}\n\nSummary:"

    response = model.generate_content(prompt)
    return response.text

