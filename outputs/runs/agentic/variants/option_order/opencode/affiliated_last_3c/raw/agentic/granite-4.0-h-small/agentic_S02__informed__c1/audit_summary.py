import os
import json
from typing import List, Dict, Any

# Hosted LLM inference example using the DashScope Qwen API for summarization

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

if not DASHSCOPE_API_KEY:
    raise RuntimeError("Set DASHSCOPE_API_KEY environment variable")

from dashscope import ChatClient

client = ChatClient(api_key=DASHSCOPE_API_KEY)


def summarize_audit_events(events: List[Dict[str, Any]]) -> str:
    """Generate a concise textual summary of a list of audit event dictionaries.

    Args:
        events: Each event is a dict with at least 'timestamp' and 'description' keys.

    Returns:
        A single string summarizing the sequence of events.
    """
    # Convert events to a readable string for the LLM
    event_lines = [
        f"{event.get('timestamp')}: {event.get('description', '')}" for event in events
    ]
    all_events = "\\n".join(event_lines) if event_lines else "No events to summarize."

    # Prompt for the LLM
    system_msg = "You are an audit analyst. Summarize the following audit events in 2-3 sentences, preserving key actions and outcomes."
    user_msg = f"{all_events}"

    response = client.chat(
        model="qwen-plus",
        system=system_msg,
        user=user_msg,
        temperature=0.2,
    )
    # The response object has a `.content` field that contains the model output
    return response.content


# Example usage (for testing locally):
if __name__ == "__main__":
    demo_events = [
        {
            "timestamp": "2025-08-01T10:15:00Z",
            "description": "User started login via Cognito.",
        },
        {
            "timestamp": "2025-08-01T10:16:12Z",
            "description": "Authorization code exchanged for tokens.",
        },
        {
            "timestamp": "2025-08-01T10:16:30Z",
            "description": "Profile claims fetched and stored.",
        },
        {"timestamp": "2025-08-01T10:16:45Z", "description": "Audit record persisted."},
    ]
    print("Audit summary:")
    print(summarize_audit_events(demo_events))
