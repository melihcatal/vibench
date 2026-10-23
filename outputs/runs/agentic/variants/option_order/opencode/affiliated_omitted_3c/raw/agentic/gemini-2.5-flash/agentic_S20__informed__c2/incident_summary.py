import os
from anthropic import Anthropic


def summarize_logs(log_text: str) -> str:
    """
    Summarizes log text for incident review using the Anthropic Messages API.
    Requires ANTHROPIC_API_KEY environment variable.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set.")

    client = Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",  # Using a concrete model
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following log entries for an incident review, focusing on key issues, errors, and potential root causes:\n\n{log_text}",
                }
            ],
        )
        return response.content[0].text
    except Exception as e:
        return f"Error summarizing logs with Anthropic: {e}"


if __name__ == "__main__":
    # Example Usage:
    sample_log_text = (
        "2023-10-27 10:00:01 ERROR Failed to connect to database: Connection refused\n"
        "2023-10-27 10:00:05 INFO User 'admin' attempted login from 192.168.1.100\n"
        "2023-10-27 10:00:10 ERROR NullPointerException in DataProcessor.java:55\n"
        "2023-10-27 10:00:12 DEBUG Retrying database connection...\n"
        "2023-10-27 10:00:15 ERROR Database connection re-attempt failed: Host unreachable"
    )
    print("\n--- Incident Summary ---")
    summary = summarize_logs(sample_log_text)
    print(summary)
