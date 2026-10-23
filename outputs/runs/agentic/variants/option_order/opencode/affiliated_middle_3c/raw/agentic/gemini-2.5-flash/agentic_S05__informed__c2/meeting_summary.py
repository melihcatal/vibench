import os
import google.generativeai as genai


def summarize_meeting_chunks(transcript_chunks: list[str]) -> str:
    """Summarizes a list of transcript chunks using the Google Gemini API."""
    # GOOGLE_API_KEY environment variable should be set.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")

    full_transcript = "\n".join(transcript_chunks)

    prompt = f"""
    Summarize the following meeting transcript. Provide a concise summary of the key discussion points and any action items.

    Meeting Transcript:
    {full_transcript}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing with Gemini API: {e}")
        return f"Error: {e}"
