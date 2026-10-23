import os
import json
from openai import OpenAI

def summarize_logs_for_incident(log_entries: list[dict]) -> str:
    """
    Summarizes a list of log entries for an incident report using OpenAI.

    Args:
        log_entries: A list of log entry dictionaries.

    Returns:
        A string containing the summary.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    # We format the logs into a string for the prompt.
    log_dump = "\n".join([json.dumps(log) for log in log_entries])
    
    if not log_dump:
        return "No log entries provided for summary."

    prompt = f"""
    The following is a list of structured logs from a production system during a potential incident.
    Please analyze these logs and provide a concise summary suitable for an incident report.
    Focus on the timeline of events, key errors, and potential root causes.

    Log Entries:
    {log_dump}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert Site Reliability Engineer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        return f"An error occurred while communicating with the OpenAI API: {e}"

if __name__ == '__main__':
    # Example usage with sample log data
    sample_logs = [
        {'timestamp': '2023-10-27T10:00:01Z', 'severity': 'INFO', 'message': 'User login successful', 'user_id': 'user_abc'},
        {'timestamp': '2023-10-27T10:02:05Z', 'severity': 'ERROR', 'message': 'Database connection failed: timeout', 'service': 'payment-service'},
        {'timestamp': '2023-10-27T10:02:15Z', 'severity': 'ERROR', 'message': 'Failed to process payment for order 12345', 'service': 'payment-service'},
        {'timestamp': '2023-10-27T10:03:00Z', 'severity': 'WARNING', 'message': 'High CPU usage detected on db-host-1', 'service': 'monitoring'},
    ]
    
    incident_summary = summarize_logs_for_incident(sample_logs)
    print("--- Incident Summary ---")
    print(incident_summary)
    print("------------------------")
