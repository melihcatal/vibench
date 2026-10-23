"""Summarize secret rotation status using an LLM."""
import os
from openai import OpenAI


def summarize_rotation_status(audit_log: str) -> str:
    """
    Uses OpenAI's GPT model to summarize a secret rotation audit log.

    Args:
        audit_log: A string containing audit events related to secret rotation.

    Returns:
        A human-readable summary of the rotation status.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Based on the following audit log for a secret, provide a brief, one-sentence summary of the last rotation attempt.
    Mention if it was successful or failed and when it happened.

    Audit Log:
    ---
    {audit_log}
    ---

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a security analyst assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=100,
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == '__main__':
    log_success = """
    [2023-10-27 10:00:00] Rotation attempt started for secret 'prod/db/main'.
    [2023-10-27 10:00:01] createSecret: Successfully created a new secret version.
    [2023-10-27 10:00:03] setSecret: Successfully attached AWSPENDING label to new version.
    [2023-10-27 10:00:15] testSecret: Database connection test with new secret successful.
    [2023-10-27 10:00:16] finishSecret: Successfully moved AWSCURRENT label to new version. Rotation complete.
    """
    success_summary = summarize_rotation_status(log_success)
    print(f"Success Scenario Summary:\n{success_summary}\n")

    log_failure = """
    [2023-10-28 12:30:00] Rotation attempt started for secret 'staging/api/payment'.
    [2023-10-28 12:30:01] createSecret: Successfully created a new secret version.
    [2023-10-28 12:30:03] setSecret: Successfully attached AWSPENDING label to new version.
    [2023-10-28 12:30:15] testSecret: Database connection test with new secret failed. Error: 'Invalid credentials'.
    [2023-10-28 12:30:16] finishSecret: Rotation failed. Reverting changes.
    """
    failure_summary = summarize_rotation_status(log_failure)
    print(f"Failure Scenario Summary:\n{failure_summary}\n")
