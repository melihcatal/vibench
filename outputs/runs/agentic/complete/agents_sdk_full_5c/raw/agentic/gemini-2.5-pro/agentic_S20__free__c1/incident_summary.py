import os
from openai import OpenAI
from typing import List

def summarize_log_incident(log_entries: List[str]) -> str:
    """
    Summarizes a list of error log entries for an incident report
    using the OpenAI GPT-4 Turbo model.

    Args:
        log_entries: A list of strings, where each string is a log message.

    Returns:
        A concise summary of the potential incident based on the logs.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAI(api_key=api_key)

    if not log_entries:
        return "No log entries provided for summary."

    # Combine log entries into a single block of text
    log_text = "\n".join(log_entries)

    # Create the prompt for the model
    prompt = f"""
    The following is a sequence of error logs from our production system. 
    Please analyze these logs and provide a concise summary of the incident.
    Focus on the likely root cause, the user impact, and the sequence of events.
    Format the summary for a technical incident review meeting.

    Log Data:
    ---
    {log_text}
    ---

    Incident Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
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
        return f"An error occurred while communicating with OpenAI: {e}"

# Example Usage:
# error_logs = [
#     'ERROR: 2023-10-27T10:00:05Z - payment-service: Database connection failed: timeout expired',
#     'ERROR: 2023-10-27T10:00:06Z - payment-service: Failed to process transaction for user_123. UID: txn_abc',
#     'ERROR: 2023-10-27T10:00:10Z - checkout-service: Payment service returned 503 Service Unavailable for order_456',
# ]
# incident_report = summarize_log_incident(error_logs)
# print(incident_report)
