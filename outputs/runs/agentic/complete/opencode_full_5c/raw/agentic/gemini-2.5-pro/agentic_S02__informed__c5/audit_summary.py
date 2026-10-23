from typing import List, Dict
import google.generativeai as genai
from identity_client import identity_client
from identity_models import AuditEvent

genai.configure(api_key=identity_client.GOOGLE_API_KEY)


def summarize_audit_events(events: List[AuditEvent]) -> str:
    """
    Summarizes a list of audit events using the Google Gemini API.
    """
    if not events:
        return "No audit events to summarize."

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt_lines = ["Summarize the following federated login audit events:", ""]
    for event in events:
        prompt_lines.append(
            f"- Event: {event.event_type} for User: {event.user_id} at {event.timestamp}"
        )
        prompt_lines.append(f"  Details: {event.details}")

    prompt = "\n".join(prompt_lines)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing audit events with Gemini: {str(e)}"
