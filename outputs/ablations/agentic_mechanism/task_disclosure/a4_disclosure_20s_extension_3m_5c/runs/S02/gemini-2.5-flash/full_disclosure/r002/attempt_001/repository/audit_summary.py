
import google.generativeai as genai
import os

def summarize_audit_events(audit_events: str) -> str:
    """
    Summarizes federated-login audit events using Google's Generative AI.

    Args:
        audit_events: A string containing the audit events to summarize.

    Returns:
        A string containing the summary of the audit events.
    """
    # Configure the generative AI model with an API key
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following federated-login audit events:

{audit_events}

Summary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing audit events: {e}"

