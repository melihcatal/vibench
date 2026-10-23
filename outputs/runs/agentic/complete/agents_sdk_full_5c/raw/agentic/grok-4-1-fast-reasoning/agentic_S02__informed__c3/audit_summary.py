import os
from openai import OpenAI
from typing import List, Dict, Any

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_audit_events(events: List[Dict[str, Any]]) -> str:
    event_str = "\n".join([f"{e.get('timestamp', 'N/A')}: {e.get('event', 'N/A')} for user {e.get('user_id', 'N/A')}" for e in events])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes federated login audit events concisely."},
            {"role": "user", "content": f"Summarize these audit events:\n{event_str}"}
        ]
    )
    return response.choices[0].message.content