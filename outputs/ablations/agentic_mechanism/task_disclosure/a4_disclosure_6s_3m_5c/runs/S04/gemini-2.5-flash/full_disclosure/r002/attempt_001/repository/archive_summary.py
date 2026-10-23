import google.generativeai as genai
import os

def summarize_transcription_results(transcription_text: str) -> str:
    """
    Summarizes transcription results using Google's Generative AI.

    Args:
        transcription_text: The full text of the transcription.

    Returns:
        A summarized version of the transcription text.
    """
    # Ensure the Google API key is set as an environment variable or passed securely.
    # For demonstration, we assume it's available as GOOGLE_API_KEY.
    # In a production environment, use more secure authentication methods.
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it to use Google Generative AI.")

    model = genai.GenerativeModel('gemini-pro')

    prompt = (
        "Please summarize the following meeting transcription. "
        "Focus on key discussion points, decisions made, and any action items. "
        "The summary should be concise and easy to read:

"
        f"{transcription_text}"
    )

    response = model.generate_content(prompt)

    return response.text
