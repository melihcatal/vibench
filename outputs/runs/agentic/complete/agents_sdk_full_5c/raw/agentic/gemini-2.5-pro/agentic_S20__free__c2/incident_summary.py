import os
import cohere
from query_error_logs import query_recent_errors

def summarize_incident_from_logs(hours: int = 4) -> str:
    """
    Fetches recent error logs and uses Cohere to generate a summary.

    Args:
        hours: The number of hours to look back for error logs.

    Returns:
        A string containing the incident summary.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    print(f"Fetching error logs from the last {hours} hours...")
    error_logs = query_recent_errors(hours=hours)

    if not error_logs:
        return "No error logs found in the specified time frame. No incident to report."

    # Format logs for the model
    log_texts = [f"[{log.timestamp}] {log.message} - PAYLOAD: {log.payload}" for log in error_logs[:20]]
    log_blob = "\n".join(log_texts)

    prompt = f"""
The following is a series of error logs from our production system. 
Please analyze these logs and provide a concise incident summary for a technical manager. 
The summary should include:
1. A brief, one-sentence title for the incident.
2. The likely root cause or the most frequent error pattern.
3. The potential impact on users or other systems.
4. Any recurring user IDs, request IDs, or services.

Here are the logs:
---
{log_blob}
---
    """

    print("Generating summary with Cohere...")
    try:
        response = co.chat(
            model='command-r',
            message=prompt,
            temperature=0.3,
        )
        summary = response.text
    except cohere.CohereError as e:
        return f"Error from Cohere API: {e}"

    return summary

if __name__ == "__main__":
    try:
        incident_summary = summarize_incident_from_logs(hours=4)
        print("\n--- Incident Summary ---")
        print(incident_summary)
        print("------------------------")
    except (ValueError, Exception) as e:
        print(f"An error occurred: {e}")
