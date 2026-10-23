import os
import google.generativeai as genai


def summarize_transcript(transcript: str, model_name: str = "gemini-pro") -> str:
    """Summarizes transcription results using the Google Gemini API.

    Args:
        transcript: The full transcript text to summarize.
        model_name: The name of the Gemini model to use (default: 'gemini-pro').

    Returns:
        A concise summary of the transcript.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel(model_name)

    prompt = (
        f"Please provide a concise summary of the following transcript:\n\n{transcript}"
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary with Gemini API: {e}")
        return f"Summary generation failed: {e}"
