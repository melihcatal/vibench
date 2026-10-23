import os
import google.generativeai as genai
from typing import List

def summarize_audit_events(events: List[str]) -> str:
    """
    Summarizes a list of federated login audit events using the Google Gemini API.

    Args:
        events: A list of strings, where each string is an audit event description.

    Returns:
        A concise summary of the audit events.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set.")

    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-pro')
    
    if not events:
        return "No audit events to summarize."

    events_text = "\n".join(f"- {event}" for event in events)
    prompt = f"""
    Please provide a concise summary of the following security audit events related to user logins. 
    Focus on identifying suspicious patterns, repeated failures, or successful but unusual access.

    Audit Events:
    {events_text}

    Summary:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary with Gemini API: {e}")
        raise
