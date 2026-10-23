import os
import google.generativeai as genai


def summarize_key_usage(audit_logs: str) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Summarize the following AWS KMS audit logs, focusing on key lifecycle events 
    (creation, deletion, rotation), cryptographic operations, and any access anomalies.

    Audit Logs:
    {audit_logs}
    
    Provide a concise summary:
    """

    response = model.generate_content(prompt)

    return response.text
