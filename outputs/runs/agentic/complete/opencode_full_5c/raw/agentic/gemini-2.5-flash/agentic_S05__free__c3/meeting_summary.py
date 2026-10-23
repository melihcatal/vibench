import google.generativeai as genai # Provider SDK import
import os

def summarize_meeting_chunk(text_chunk: str):
    """Summarizes a chunk of live meeting transcript using Google Generative AI (Gemini/PaLM API)."""
    # Ensure GOOGLE_API_KEY is set in environment variables
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable not set."

    model = genai.GenerativeModel('gemini-pro') # Provider-specific model ID/family

    prompt = f"Summarize the following meeting transcript chunk concisely: \""""{text_chunk}"""""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error summarizing: {e}"
