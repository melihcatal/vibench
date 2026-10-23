import os
import google.generativeai as genai
from typing import Dict, Any

def summarize_message_results(results: Dict[str, Any]) -> str:
    """Summarizes message processing results using Google's Generative AI (Gemini Pro).

    Args:
        results: A dictionary containing the message processing results.

    Returns:
        A string containing the summary of the results.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Please summarize the following message processing results concisely: {results}"

    response = model.generate_content(prompt)
    return response.text
