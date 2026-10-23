import os
import google.generativeai as genai
from typing import List, Dict


def summarize_audit_events(events: List[Dict]) -> str:
    """
    Summarizes a list of audit events using the Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = "Summarize the following federated login audit events:\n\n"
    for event in events:
        prompt += f"- User: {event.get('user_id', 'N/A')}, Event: {event.get('event_type', 'N/A')}, Timestamp: {event.get('timestamp', 'N/A')}\n"

    prompt += "\nProvide a brief summary of the activity."

    response = model.generate_content(prompt)
    return response.text
