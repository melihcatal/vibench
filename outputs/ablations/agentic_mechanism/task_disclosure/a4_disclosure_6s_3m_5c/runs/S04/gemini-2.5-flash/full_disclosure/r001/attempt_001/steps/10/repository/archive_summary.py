import os
import google.generativeai as genai

def summarize_transcription(transcription_text: str) -> str:
    """
    Summarizes transcription results using Google's Generative AI.

    Args:
        transcription_text: The full text of the transcription to summarize.

    Returns:
        A summarized version of the transcription text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Please summarize the following transcription:

{transcription_text}"

    response = model.generate_content(prompt)
    return response.text.strip()
