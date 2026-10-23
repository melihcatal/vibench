import os
import openai
from datetime import datetime, timedelta

def summarize_audit_events(events: list[dict]) -> str:
    """
    Summarizes a list of federated login audit events using OpenAI.

    Args:
        events: A list of audit event dictionaries.

    Returns:
        A natural language summary of the events.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt_content = f"""
    Summarize the following federated login audit events. Focus on identifying
    any suspicious patterns, such as multiple failed logins followed by a success,
    logins from multiple distinct IP addresses for the same user, or unusual times.

    Events:
    {events}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an security analyst's assistant."},
                {"role": "user", "content": prompt_content},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing events: {e}"

# Example usage:
# if __name__ == '__main__':
#     sample_events = [
#         {'timestamp': (datetime.now() - timedelta(minutes=10)).isoformat(), 'user_id': 'user_123', 'event': 'login_failed', 'ip_address': '198.51.100.1'},
#         {'timestamp': (datetime.now() - timedelta(minutes=9)).isoformat(), 'user_id': 'user_123', 'event': 'login_failed', 'ip_address': '198.51.100.1'},
#         {'timestamp': (datetime.now() - timedelta(minutes=8)).isoformat(), 'user_id': 'user_123', 'event': 'login_success', 'ip_address': '198.51.100.1'},
#         {'timestamp': (datetime.now() - timedelta(minutes=5)).isoformat(), 'user_id': 'user_123', 'event': 'login_success', 'ip_address': '203.0.113.55'},
#         {'timestamp': (datetime.now() - timedelta(minutes=2)).isoformat(), 'user_id': 'user_456', 'event': 'login_success', 'ip_address': '192.0.2.14'},
#     ]
#     summary = summarize_audit_events(sample_events)
#     print(summary)

