import os
from openai import OpenAI
from typing import List
from identity_models import AuditEvent

def summarize_federated_login_audits(events: List[AuditEvent]) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY not set")
    events_text = '\n'.join([
        f"{e.timestamp.isoformat()}: {e.event_type} (user_id={e.user_id or 'N/A'}, client={e.client_id}, success={e.success})"
        for e in events
    ])
    messages = [
        {
            "role": "system",
            "content": "Summarize the following federated login audit events. Highlight key activities, successes/failures, patterns, and any anomalies."
        },
        {"role": "user", "content": events_text}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
