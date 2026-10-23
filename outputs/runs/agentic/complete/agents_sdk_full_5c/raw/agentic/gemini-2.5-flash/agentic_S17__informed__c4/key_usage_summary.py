import google.generativeai as genai
import os

def summarize_key_usage(audit_logs: str) -> str:
    """
    Summarizes key usage and crypto events using Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the following key usage and cryptographic event logs:

{audit_logs}

Provide a concise summary highlighting key activities, potential anomalies, and overall usage patterns.
"""

    response = model.generate_content(prompt)
    return response.text

