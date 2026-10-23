import os
import google.generativeai as genai
from speech_models import SummaryResult

def summarize_meeting_chunk(text_chunk: str) -> SummaryResult:
    """Summarizes a chunk of meeting transcript using Google's Generative AI (Gemini Pro)."""
    # Ensure GOOGLE_API_KEY environment variable is set for Generative AI
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Use a specific generative model, e.g., 'gemini-pro' for text-only tasks.
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please summarize the following meeting transcript chunk:

{text_chunk}

Summary:"

    try:
        response = model.generate_content(prompt)
        summary_text = response.text
        return SummaryResult(summary=summary_text)
    except Exception as e:
        print(f"Error summarizing with Generative AI: {e}")
        return SummaryResult(summary="") # Return empty summary on error
