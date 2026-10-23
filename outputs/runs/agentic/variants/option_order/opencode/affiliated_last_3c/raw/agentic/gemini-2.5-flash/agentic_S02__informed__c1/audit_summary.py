import os
import google.generativeai as genai
from identity_client import config
from identity_models import AuditEvent

def summarize_audit_events(events: list[AuditEvent]) -> str:
    genai.configure(api_key=config.GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    event_strings = [
        f"Event ID: {event.event_id}, Timestamp: {event.timestamp}, User ID: {event.user_id}, Type: {event.event_type}, Details: {event.details}"
        for event in events
    ]
    prompt = "Summarize the following federated login audit events, highlighting any unusual activity or potential security concerns:

" + "\n".join(event_strings)

    response = model.generate_content(prompt)
    return response.text
