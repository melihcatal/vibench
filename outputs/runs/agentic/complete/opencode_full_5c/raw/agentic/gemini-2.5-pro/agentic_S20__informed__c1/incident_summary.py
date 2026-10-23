import os
from openai import OpenAI
from typing import List


def summarize_incident(error_logs: List[str]) -> str:
    """
    Summarizes a list of error log messages for an incident report using OpenAI.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    log_content = "\n".join(error_logs)

    if not log_content.strip():
        return "No error logs provided for summary."

    prompt = f"""
    The following are error logs from a production incident. Please provide a concise summary of the incident.
    Identify the potential root cause, impact, and timeline of events based on these logs.

    Logs:
    {log_content}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing logs for incident response.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=500,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        print(f"An error occurred while calling OpenAI API: {e}")
        return "Failed to generate incident summary."


if __name__ == "__main__":
    # Example usage:
    # Ensure OPENAI_API_KEY is set in your environment
    sample_errors = [
        "2023-10-27T10:00:15Z ERROR: Database connection failed: timeout expired",
        "2023-10-27T10:00:15Z ERROR: Failed to process user request for user_id=abc, reason: ConnectionPool depleted",
        "2023-10-27T10:01:20Z ERROR: Database connection failed: timeout expired",
        "2023-10-27T10:02:05Z ERROR: API endpoint /api/v1/data returned 503",
    ]
    incident_summary = summarize_incident(sample_errors)
    print("--- Incident Summary ---")
    print(incident_summary)
