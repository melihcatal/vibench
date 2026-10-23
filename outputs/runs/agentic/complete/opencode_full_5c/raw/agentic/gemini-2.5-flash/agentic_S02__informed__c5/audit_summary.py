import os
import google.generativeai as genai

def summarize_audit_events(audit_events: str) -> str:
    """Summarizes federated-login audit events using the Google Gemini API.

    Args:
        audit_events: A string containing the audit events to summarize.

    Returns:
        A summary of the audit events.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Using a specific model known for text generation
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro as a concrete model identifier

    prompt = f"Please summarize the following federated login audit events:

{audit_events}

Summary:"

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example Usage:
    # export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    example_events = (
        "User 'john.doe@example.com' successfully logged in using Auth0 on 2024-04-18 at 10:00:00. "
        "IP Address: 192.168.1.100. MFA challenge successful. "
        "User 'jane.smith@example.com' failed login attempt (invalid credentials) on 2024-04-18 at 10:05:00. "
        "IP Address: 192.168.1.101."
    )
    try:
        summary = summarize_audit_events(example_events)
        print("Audit Summary:")
        print(summary)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
