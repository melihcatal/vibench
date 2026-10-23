import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_incident_logs(error_logs: List[Dict[str, Any]]) -> str:
    """Summarizes error log findings for incident review using the Google Gemini API."""
    # Configure the Gemini API client
    # Ensure GOOGLE_API_KEY environment variable is set
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable not set."

    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text generation

    if not error_logs:
        return "No error logs provided for summarization."

    # Format logs for the prompt
    log_strings = []
    for log in error_logs:
        # Assuming log is a dict or has a way to get relevant info
        # If using observability_models.LogEntry, adapt accordingly
        timestamp = log.get('timestamp', 'N/A')
        severity = log.get('severity', 'N/A')
        message = log.get('jsonPayload', {}).get('message', log.get('textPayload', 'No message'))
        component = log.get('jsonPayload', {}).get('component', 'N/A')
        log_strings.append(f"[{timestamp}] [{severity}] [{component}] {message}")
    
    logs_text = "\n".join(log_strings)

    prompt = f"""Review the following error logs and provide a concise summary suitable for an incident review meeting. 
    Highlight key issues, potential root causes, and affected components. If possible, suggest next steps.

Logs:
{logs_text}

Incident Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

if __name__ == "__main__":
    # This example requires mock log entries or integration with query_error_logs.py
    # For a real scenario, you'd fetch logs first.
    sample_error_logs = [
        {
            "timestamp": "2023-10-27T10:00:00Z",
            "severity": "ERROR",
            "jsonPayload": {"message": "Database connection failed", "component": "database"}
        },
        {
            "timestamp": "2023-10-27T10:01:05Z",
            "severity": "ERROR",
            "jsonPayload": {"message": "Service 'user-auth' unresponsive", "component": "authentication"}
        },
        {
            "timestamp": "2023-10-27T10:02:30Z",
            "severity": "WARNING",
            "jsonPayload": {"message": "High CPU usage on worker-01", "component": "compute"}
        }
    ]

    summary = summarize_incident_logs(sample_error_logs)
    print(summary)
