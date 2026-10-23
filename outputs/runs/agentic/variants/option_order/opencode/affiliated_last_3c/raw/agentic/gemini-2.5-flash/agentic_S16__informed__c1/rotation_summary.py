import os
import google.generativeai as genai

def summarize_rotation_status(rotation_notes: str) -> str:
    """Summarizes secret rotation status using the Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following secret rotation notes in a concise manner:
{rotation_notes}"
    response = model.generate_content(prompt)
    return response.text

