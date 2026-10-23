import os
import google.generativeai as genai


def summarize_transcription_results(transcript_text: str) -> str:
    """
    Summarizes transcription results using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model identifier

    prompt = f"Please provide a concise summary of the following transcript:\n\n{transcript_text}\n\nSummary:"

    response = model.generate_content(prompt)
    return response.text
