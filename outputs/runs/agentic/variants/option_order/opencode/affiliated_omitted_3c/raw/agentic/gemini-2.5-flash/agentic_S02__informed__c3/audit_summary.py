import os
from anthropic import Anthropic


def summarize_audit_events(audit_events: str) -> str:
    """Summarizes federated-login audit events using Anthropic's Claude model."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = Anthropic(api_key=api_key)

    # Using a recent Claude model, e.g., "claude-3-opus-20240229"
    # You might choose a different model based on your needs (e.g., Haiku for cost-effectiveness)
    model_name = "claude-3-opus-20240229"

    prompt = f"""Please summarize the following federated login audit events:

{audit_events}

Provide a concise summary highlighting any unusual activity or potential security concerns.
"""

    response = client.messages.create(
        model=model_name, max_tokens=500, messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


# Example usage (not part of the file, just for demonstration):
# if __name__ == "__main__":
#     os.environ["ANTHROPIC_API_KEY"] = "YOUR_ANTHROPIC_API_KEY"
#     sample_audit_events = """
#     [Event 1] User 'alice' logged in from IP 192.168.1.100 at 2023-10-27 10:00:00. Provider: Auth0.
#     [Event 2] User 'bob' failed login attempt from IP 203.0.113.5 at 2023-10-27 10:05:00. Reason: Invalid credentials.
#     [Event 3] User 'alice' changed password from IP 192.168.1.100 at 2023-10-27 10:15:00.
#     [Event 4] User 'charlie' logged in from IP 198.51.100.22 unexpectedly at 3 AM from an unknown device.
#     """
#     try:
#         summary = summarize_audit_events(sample_audit_events)
#         print("Audit Summary:")
#         print(summary)
#     except ValueError as e:
#         print(f"Configuration Error: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
