from observability_client import get_anthropic_client
from typing import List, Dict
import os

def summarize_incident(error_logs: List[Dict]) -> str:
    client = get_anthropic_client()
    
    log_messages = [log.get("@message", "") for log in error_logs]
    log_text = "\n".join(log_messages)

    if not log_text:
        return "No error logs provided for summarization."

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229", # Using a powerful Claude 3 model for summarization
            max_tokens=1024,
            messages=[
                {"role": "user", "content": f"Please summarize the following error logs for an incident review. Focus on identifying the root cause, affected components, and potential impact:\n\n{log_text}"}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error summarizing incident: {e}")
        raise
