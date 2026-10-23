import os
from openai import OpenAI
from typing import List
from identity_models import AuditEvent

def summarize_audit_events(events: List[AuditEvent]) -> str:
    """
    Summarizes a list of federated login audit events using OpenAI's GPT models.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    if not events:
        return "No audit events to summarize."
        
    event_descriptions = []
    for event in events:
        details = event.details or {}
        event_descriptions.append(
            f"- At {event.timestamp}, user {event.user_id} triggered {event.event_type} "
            f"from IP {event.ip_address}. Details: {details}"
        )
    
    prompt_text = "\n".join(event_descriptions)
    
    system_prompt = (
        "You are a security analyst assistant. Your task is to summarize a list of "
        "federated login audit events. Focus on identifying suspicious patterns, "
        "repeated failures, or unusual access times/locations. Provide a concise summary."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please summarize the following audit events:\n{prompt_text}"}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred while summarizing audit events: {e}")
        raise
