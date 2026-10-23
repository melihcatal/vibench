import os
import google.generativeai as genai
from messaging_models import MessageSummaryRequest


def summarize_message(request: MessageSummaryRequest) -> str:
    """Summarizes message processing results using the Google Gemini API.

    Args:
        request: A MessageSummaryRequest object containing the text to summarize.

    Returns:
        A string containing the summary of the message.
    """
    # Configure the Gemini API client
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Choose a model, e.g., 'gemini-pro'
    model = genai.GenerativeModel("gemini-pro")

    try:
        response = model.generate_content(
            f"Please provide a concise summary of the following message content: {request.message_text}"
        )
        return response.text
    except Exception as e:
        print(f"Error summarizing message with Gemini API: {e}")
        return f"Error: Could not summarize message. {e}"
