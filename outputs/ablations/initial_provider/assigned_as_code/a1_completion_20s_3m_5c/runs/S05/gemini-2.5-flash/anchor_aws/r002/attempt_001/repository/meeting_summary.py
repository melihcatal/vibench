import os
import google.generativeai as genai

def summarize_meeting_transcript(transcript_chunks: list[str]) -> str:
    # Configure the Google Generative AI client
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    full_transcript = " ".join(transcript_chunks)

    prompt = f"Summarize the following meeting transcript:\n\n{full_transcript}\n\nSummary:"

    response = model.generate_content(prompt)
    return response.text
