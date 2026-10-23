import google.generativeai as genai
import os

def summarize_transcript(transcript_chunks: list[str]) -> str:
    # Ensure the API key is set as an environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    full_transcript = " ".join(transcript_chunks)

    prompt = f"Summarize the following meeting transcript:\n\n{full_transcript}\n\nSummary:"

    response = model.generate_content(prompt)
    return response.text
