import os
import google.generativeai as genai
from typing import List, Dict, Any
from identity_client import get_google_gemini_config
from identity_models import AuditEvent


def summarize_audit_events(events: List[AuditEvent]) -> str:
    config = get_google_gemini_config()
    if not config.api_key:
        raise ValueError("Google Gemini API key not configured.")

    genai.configure(api_key=config.api_key)
    model = genai.GenerativeModel("gemini-pro")

    event_strings = []
    for event in events:
        event_strings.append(
            f"Event ID: {event.event_id}, Timestamp: {event.timestamp}, User ID: {event.user_id}, Type: {event.event_type}, Details: {event.details}"
        )

    prompt = """
    Summarize the following federated login audit events. Highlight any unusual activities or patterns.

    Audit Events:
    """ + "\n".join(event_strings)

    response = model.generate_content(prompt)
    return response.text
