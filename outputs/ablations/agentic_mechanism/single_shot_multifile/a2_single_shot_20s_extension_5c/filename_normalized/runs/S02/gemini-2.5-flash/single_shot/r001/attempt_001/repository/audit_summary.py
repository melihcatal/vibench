import os
import openai
from identity_models import AuditRecord
from typing import List

def summarize_audit_events(events: List[AuditRecord]) -> str:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI()

    event_strings = [str(event) for event in events]
    combined_events_text = "\n".join(event_strings)

    prompt_messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes security audit logs. Focus on key events, anomalies, and user activities."},
        {"role": "user", "content": f"Summarize the following federated login audit events:\n\n{combined_events_text}"}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt_messages,
        max_tokens=200
    )
    
    summary = response.choices[0].message.content.strip()
    return summary
