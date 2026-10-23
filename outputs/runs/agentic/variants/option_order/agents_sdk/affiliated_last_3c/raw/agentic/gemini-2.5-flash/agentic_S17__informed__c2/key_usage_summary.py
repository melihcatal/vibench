import google.generativeai as genai
import os

def summarize_key_usage(crypto_events_log: str) -> str:
    """
    Summarizes key usage and crypto events using the Google Gemini API.

    Args:
        crypto_events_log: A string containing raw crypto event logs.

    Returns:
        A summarized string of key usage.
    """
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following cryptographic key usage and events:

{crypto_events_log}

Summary:"
    response = model.generate_content(prompt)
    return response.text
