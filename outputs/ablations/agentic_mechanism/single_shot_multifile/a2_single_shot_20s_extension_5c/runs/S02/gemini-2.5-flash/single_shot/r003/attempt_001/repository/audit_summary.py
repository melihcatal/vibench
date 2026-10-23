import os
import anthropic

def summarize_audit_events(events: list[dict], user_id: str) -> str:
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    client = anthropic.Anthropic(api_key=anthropic_api_key)
    
    event_strings = [f"Event Type: {e.get('event_type')}, Timestamp: {e.get('timestamp')}, Details: {e.get('details')}" for e in events]
    context_str = "\n".join(event_strings)

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[
            {"role": "user", "content": f"Summarize the following login audit events for user ID {user_id}. Focus on key actions and any anomalies:\n\n{context_str}"
            }
        ]
    )
    return response.content[0].text
