import os
import google.generativeai as genai


def summarize_transcript_chunk(transcript_chunk: str) -> str:
    """
    Summarizes a chunk of a meeting transcript using the Google Gemini API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following meeting transcript chunk:\n\n{transcript_chunk}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return ""
