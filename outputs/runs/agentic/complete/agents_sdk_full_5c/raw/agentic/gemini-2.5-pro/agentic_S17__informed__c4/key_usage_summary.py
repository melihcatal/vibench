"""Summarizes key usage events using an LLM."""
import os
import json
from openai import OpenAI

def summarize_key_events(audit_events: list[dict]) -> str:
    """
    Uses OpenAI's GPT model to generate a human-readable summary
    of cryptographic key usage events.

    Args:
        audit_events: A list of dictionaries representing audit events.

    Returns:
        A natural language summary of the events.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    The following is a list of JSON objects representing cryptographic key audit events.
    Please provide a brief, human-readable summary of this activity.
    Focus on the number of operations, the types of operations (e.g., Encrypt, Decrypt),
    and any potential anomalies or notable patterns.

    Audit Events:
    {json.dumps(audit_events, indent=2)}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful security analyst assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=250,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        return f"An error occurred while communicating with the OpenAI API: {e}"

# Example Usage (for demonstration if run directly)
if __name__ == '__main__':
    mock_events = [
        {"eventId": "evt-001", "eventTime": "2023-10-27T10:00:00Z", "keyId": "key-123", "operation": "Encrypt"},
        {"eventId": "evt-002", "eventTime": "2023-10-27T10:05:00Z", "keyId": "key-123", "operation": "Decrypt"},
        {"eventId": "evt-003", "eventTime": "2023-10-27T10:15:00Z", "keyId": "key-456", "operation": "Sign"},
        {"eventId": "evt-004", "eventTime": "2023-10-27T11:00:00Z", "keyId": "key-123", "operation": "Encrypt"},
        {"eventId": "evt-005", "eventTime": "2023-10-27T12:30:00Z", "keyId": "key-123", "operation": "DecryptFailure"},
    ]
    if os.environ.get("OPENAI_API_KEY"):
        print("Generating key usage summary...")
        summary_text = summarize_key_events(mock_events)
        print("\n--- Summary ---")
        print(summary_text)
        print("-----------------")
    else:
        print("Skipping example: OPENAI_API_KEY environment variable not set.")
