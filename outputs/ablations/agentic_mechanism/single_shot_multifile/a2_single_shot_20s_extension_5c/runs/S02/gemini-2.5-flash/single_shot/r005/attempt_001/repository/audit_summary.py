import os
from openai import OpenAI
from identity_models import AuditRecord
from typing import List

def summarize_login_audit_events(events: List[AuditRecord]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    event_strings = []
    for event in events:
        event_strings.append(f"Timestamp: {event['timestamp']}, Type: {event['event_type']}, User: {event['user_id']}, IP: {event['ip_address']}, Details: {event['details']}")
    
    prompt = (
        "Summarize the following federated login audit events, highlighting any unusual activity or trends.\n\n"
        + "\n".join(event_strings)
        + "\n\nSummary:"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes audit logs."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
