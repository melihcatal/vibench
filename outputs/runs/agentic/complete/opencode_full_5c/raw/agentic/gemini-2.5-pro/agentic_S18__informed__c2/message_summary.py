import os
import google.generativeai as genai
from messaging_models import ProcessingResult


def message_summary(results: ProcessingResult) -> str:
    """
    Summarizes message processing results using Gemini.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following message processing result: {results}"

    response = model.generate_content(prompt)

    return response.text
