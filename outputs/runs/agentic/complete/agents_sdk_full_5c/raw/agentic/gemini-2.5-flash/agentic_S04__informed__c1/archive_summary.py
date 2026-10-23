import os
import google.generativeai as genai

def summarize_transcript(transcript_text: str) -> str:
    """
    Summarizes transcription results using the Google Gemini API.

    Args:
        transcript_text: The full text of the transcript to summarize.

    Returns:
        A string containing the summary.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=google_api_key)

    # Using a specific model, e.g., gemini-pro
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please provide a concise summary of the following meeting transcript:\n\n{transcript_text}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing transcript with Gemini API: {e}")
        return f"Error: {e}"
