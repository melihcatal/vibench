
import os
from openai import OpenAI
from typing import List, Dict, Any

def summarize_incident_logs(error_logs: List[Dict[str, Any]]) -> str:
    """
    Summarizes a list of error log dictionaries for an incident report
    using the OpenAI API.

    Args:
        error_logs: A list of dictionaries, where each dictionary represents an error log.

    Returns:
        A string containing a summary of the incident.
    """
    if not error_logs:
        return "No error logs provided to summarize."

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    log_dump = "\n".join([str(log) for log in error_logs])

    prompt = f"""
    The following is a dump of error logs from a production system during a potential incident.
    Please analyze these logs and provide a concise summary for an incident report.
    The summary should include:
    1. A brief, one-sentence overview of the primary issue.
    2. A potential root cause if evident from the logs.
    3. The timeline of key error events.
    4. The scope of impact (e.g., specific services, user IDs).

    Log Data:
    ---
    {log_dump}
    ---
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert Site Reliability Engineer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        return f"Failed to generate incident summary: {e}"


if __name__ == '__main__':
    # Example error logs
    sample_errors = [
        {'timestamp': '2023-10-27T10:00:05Z', 'severity': 'ERROR', 'payload': {'message': 'Database connection timeout', 'service': 'user-db-connector', 'host': 'prod-db-1'}},
        {'timestamp': '2023-10-27T10:00:15Z', 'severity': 'ERROR', 'payload': {'message': 'Failed to execute query', 'service': 'user-service', 'error': 'Query timeout'}},
        {'timestamp': '2023-10-27T10:01:20Z', 'severity': 'ERROR', 'payload': {'message': 'Database connection timeout', 'service': 'user-db-connector', 'host': 'prod-db-1'}},
        {'timestamp': '2023-10-27T10:02:00Z', 'severity': 'CRITICAL', 'payload': {'message': 'Circuit breaker opened for database connections', 'service': 'api-gateway'}},
    ]
    
    incident_summary = summarize_incident_logs(sample_errors)
    print("--- Incident Summary ---")
    print(incident_summary)
