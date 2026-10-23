import os
from openai import OpenAI
from security_models import AuditEvent
from typing import List

def generate_key_usage_summary(events: List[AuditEvent]) -> str:
    """
    Generates a human-readable summary of key usage events using OpenAI.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt_content = "Please summarize the following cryptographic key usage events in a brief report:\n\n"
    for event in events:
        prompt_content += (
            f"- Event: {event.operation} on key {event.key_id} by {event.identity} "
            f"at {event.timestamp}. Status: {event.status}.\n"
        )
    prompt_content += "\nSummary:"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a security analyst assistant providing clear summaries of audit logs.",
                },
                {"role": "user", "content": prompt_content},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating summary with OpenAI: {e}")
        raise
