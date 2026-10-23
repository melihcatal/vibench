import os
from openai import OpenAI


def summarize_errors_for_incident(error_logs: list[str]) -> str:
    """
    Uses OpenAI's GPT model to summarize a list of error log messages
    for an incident report.
    """
    if not error_logs:
        return "No error logs provided for summary."

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    log_content = "\n".join(error_logs)
    prompt = f"""
    The following is a list of error logs from a production system during an incident.
    Please provide a concise summary of the issues. Identify patterns, root causes,
    and the potential user impact.

    Error Logs:
    ---
    {log_content}
    ---

    Summary:
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for summarizing technical incident data.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=500,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    sample_errors = [
        "ERROR: Database connection timeout on host db-prod-1. User 'user-abc', transaction 'txn-123'.",
        "ERROR: NullPointerException at com.example.UserService.getUserProfile(UserService.java:112) for userId 'user-def'.",
        "ERROR: Database connection timeout on host db-prod-1. User 'user-ghi', transaction 'txn-456'.",
        "ERROR: API call to payment-gateway failed with 503 Service Unavailable.",
        "ERROR: NullPointerException at com.example.UserService.getUserProfile(UserService.java:112) for userId 'user-jkl'.",
    ]
    try:
        summary = summarize_errors_for_incident(sample_errors)
        print("--- Incident Summary ---")
        print(summary)
    except ValueError as e:
        print(e)
