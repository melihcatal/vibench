import os
from typing import List, Dict, Any
from openai import OpenAI

def summarize_logins(audit_events: List[Dict[str, Any]]) -> str:
    """
    Summarizes a list of federated login audit events using an LLM.

    Args:
        audit_events: A list of dictionaries, where each dictionary
                      represents a login event.

    Returns:
        A human-readable summary of the login activity.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    if not audit_events:
        return "No login events to summarize."

    # Convert event dictionaries to a string format for the prompt
    events_str = "\n".join([str(event) for event in audit_events])

    prompt = f"""
    The following is a list of audit events for federated user logins.
    Please provide a brief, human-readable summary of the activity.
    Focus on the number of successful logins, number of failures,
    unique users, and any unusual patterns.

    Audit Events:
    {events_str}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an audit assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=250,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        # In a real app, log this error
        print(f"Error calling OpenAI API: {e}")
        return "Error: Could not generate summary due to an API issue."
