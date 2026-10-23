import os
from typing import List, Dict, Any
import openai

from identity_client import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def summarize_audit_events(audit_events: List[Dict[str, Any]]) -> str:
    """Summarizes a list of federated login audit events using OpenAI's GPT-3.5-turbo."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    event_texts = [f"Event Type: {event.get('event_type')}, User ID: {event.get('user_id')}, Timestamp: {event.get('timestamp')}, Details: {event.get('details')}"
                   for event in audit_events]
    
    prompt = """Summarize the following federated login audit events, highlighting key activities, potential issues, or trends:

""" + "\n".join(event_texts)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that summarizes audit logs."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()
