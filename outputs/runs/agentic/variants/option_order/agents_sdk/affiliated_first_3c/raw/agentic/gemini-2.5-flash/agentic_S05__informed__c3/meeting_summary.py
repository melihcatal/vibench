import os
import google.generativeai as genai

# Configure the Gemini API client
# Ensure GOOGLE_API_KEY environment variable is set
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

def summarize_meeting_transcript(transcript_chunks: list[str]) -> str:
    """Summarizes live meeting transcript chunks using the Gemini API (gemini-pro model)."""
    model = genai.GenerativeModel('gemini-pro')

    full_transcript = " ".join(transcript_chunks)

    prompt = f"""Please summarize the following meeting transcript:

{full_transcript}

Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing with Gemini API: {e}")
        return f"Error: {e}"
