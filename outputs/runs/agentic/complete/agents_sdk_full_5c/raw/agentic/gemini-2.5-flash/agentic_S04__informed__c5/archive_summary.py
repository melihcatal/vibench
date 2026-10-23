import os
import google.generativeai as genai

def summarize_transcript(transcript_text: str, model_name: str = "gemini-pro") -> str:
    """Summarizes a transcript using the Google Gemini API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    prompt = f"Please provide a concise summary of the following transcript:

{transcript_text}

Summary:"

    response = model.generate_content(prompt)
    if response.candidates and response.candidates[0].content.parts:
        return response.candidates[0].content.parts[0].text
    return ""
