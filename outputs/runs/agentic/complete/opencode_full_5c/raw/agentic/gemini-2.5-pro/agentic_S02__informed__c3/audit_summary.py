import os
import google.generativeai as genai
from typing import List
from identity_models import AuditEvent


def summarize_audit_events(events: List[AuditEvent]) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt_parts = [
        "Summarize the following login audit events in a brief paragraph. Focus on any unusual patterns or repeated failures.",
    ]
    for event in events:
        event_str = f"- Timestamp: {event.timestamp}, User: {event.user_id}, Event: {event.event_type}, Details: {event.details}"
        prompt_parts.append(event_str)

    prompt = "\n".join(prompt_parts)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"
