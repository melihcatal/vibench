"""
Uses a large language model to summarize federated login audit events.
This example uses the Google Gemini API.
"""
import os
import google.generativeai as genai
from typing import List
from identity_models import LoginEvent

def summarize_login_events(events: List[LoginEvent]) -> str:
    """
    Generates a natural language summary of login events using Google Gemini.

    Args:
        events: A list of LoginEvent objects.

    Returns:
        A string containing the summary.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    # Select the model, e.g., 'gemini-1.5-flash'
    model = genai.GenerativeModel('gemini-pro')

    prompt_lines = [
        "Please provide a concise summary of the following user login audit events.",
        "Highlight any suspicious patterns, such as multiple failed logins followed by a success, or logins from multiple IP addresses for the same user.",
        "\n--- AUDIT EVENTS ---\n"
    ]

    for event in events:
        status = "SUCCESS" if event.success else f"FAILURE ({event.error_message})"
        line = f"- User '{event.user_id}' login from {event.provider} at {event.timestamp} from IP {event.ip_address}. Status: {status}"
        prompt_lines.append(line)

    prompt = "\n".join(prompt_lines)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

# Example Usage:
# if __name__ == '__main__':
#     from datetime import datetime, timedelta
#     import uuid
#     # Sample login events
#     test_events = [
#         LoginEvent(event_id=str(uuid.uuid4()), user_id="user-123", provider="auth0", timestamp=(datetime.now() - timedelta(minutes=10)).isoformat(), ip_address="198.51.100.1", success=False, error_message="Invalid credentials"),
#         LoginEvent(event_id=str(uuid.uuid4()), user_id="user-123", provider="auth0", timestamp=(datetime.now() - timedelta(minutes=9)).isoformat(), ip_address="198.51.100.1", success=True),
#         LoginEvent(event_id=str(uuid.uuid4()), user_id="user-456", provider="google", timestamp=(datetime.now() - timedelta(minutes=5)).isoformat(), ip_address="203.0.113.25", success=True),
#         LoginEvent(event_id=str(uuid.uuid4()), user_id="user-123", provider="auth0", timestamp=(datetime.now() - timedelta(minutes=2)).isoformat(), ip_address="10.0.0.5", success=True),
#     ]
#     summary = summarize_login_events(test_events)
#     print("--- Generated Audit Summary ---")
#     print(summary)
