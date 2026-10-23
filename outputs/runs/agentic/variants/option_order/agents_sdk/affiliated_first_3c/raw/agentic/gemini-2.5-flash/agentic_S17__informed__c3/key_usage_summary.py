import os
import google.generativeai as genai

def summarize_key_usage(log_data: str) -> str:
    # Configure the Gemini API client
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Initialize the generative model with a concrete model identifier
    model = genai.GenerativeModel('gemini-pro')

    prompt = (
        "Summarize the following key management system (KMS) and cryptographic event logs. "
        "Identify key usage patterns, potential anomalies, and critical security events. "
        "Focus on who accessed what keys, what operations were performed (encrypt, decrypt, sign, verify), and from where."
        "\\n\\nLog Data:\n" + log_data
    )

    response = model.generate_content(prompt)

    return response.text
