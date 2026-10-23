import os
from openai import OpenAI
from identity_models import AuditRecord
from typing import List

def summarize_audit_events(audit_events: List[AuditRecord]) -> str:
    """Summarizes a list of federated-login audit events using OpenAI's GPT models."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"))

    event_strings = []
    for event in audit_events:
        event_strings.append(
            f"Event Type: {event.event_type}, User: {event.user_id}, Provider: {event.provider_id}, "
            f"Timestamp: {event.timestamp}, Details: {event.details}"
        )
    
    prompt = """
    Summarize the following federated login audit events. 
    Highlight any unusual activity, frequent login failures, or notable successful logins.

    Audit Events:
    """ + "\n".join(event_strings)

    response = client.chat.completions.create(
        model="gpt-4o-mini", # Using a cost-effective model for summarization
        messages=[
            {"role": "system", "content": "You are an audit event summarizer."}, 
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content
