import os
from openai import OpenAI
from typing import List
from security_models import AuditRecord

def summarize_rotation_events(events: List[AuditRecord]) -> str:
    """
    Uses an OpenAI model to summarize a list of secret rotation audit events.

    Args:
        events: A list of AuditRecord objects.

    Returns:
        A string containing a summary of the events.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    event_descriptions = [
        f"- At {evt.event_time}, user '{evt.user}' performed '{evt.action}' on '{evt.secret_name}'. Notes: {evt.notes}"
        for evt in events
    ]
    
    prompt_text = "Please summarize the following secret rotation activities:\n" + "\n".join(event_descriptions)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful security analyst assistant."},
                {"role": "user", "content": prompt_text},
            ]
        )
        summary = response.choices[0].message.content
        return summary.strip()

    except Exception as e:
        print(f"An error occurred while communicating with OpenAI: {e}")
        return "Could not generate summary due to an API error."
