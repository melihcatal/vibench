import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_incident_logs(incident_id: str, error_logs: List[Dict[str, Any]]) -> str:
    """Summarizes error-log findings for incident review using the Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    # Format logs into a readable string for the LLM
    log_strings = []
    for log in error_logs:
        log_strings.append(f"Timestamp: {log.get('timestamp', 'N/A')}, Severity: {log.get('severity', 'N/A')}, LogName: {log.get('log_name', 'N/A')}, Payload: {log.get('payload', 'N/A')}")

    logs_text = "\n".join(log_strings)

    prompt = f"""Review the following error logs for incident {incident_id} and provide a concise summary. 
Identify the main issues, potential root causes, and any recurring patterns. Highlight critical information for an incident responder. 

Error Logs:
{logs_text}

Incident Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing logs: {e}"

if __name__ == "__main__":
    # Example usage (replace with actual logs from query_error_logs.py output)
    # Set GOOGLE_API_KEY environment variable
    if os.getenv("GOOGLE_API_KEY") is None:
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        sample_incident_id = "INC-2023-11-01-001"
        sample_error_logs = [
            {
                "timestamp": "2023-11-01T10:00:00Z",
                "severity": "ERROR",
                "log_name": "my-app-logs",
                "payload": {"message": "Database connection failed", "db_host": "prod-db-01", "error_code": 500}
            },
            {
                "timestamp": "2023-11-01T10:01:05Z",
                "severity": "ERROR",
                "log_name": "my-app-logs",
                "payload": {"message": "Service Unavailable: upstream timeout", "service": "user-service"}
            },
            {
                "timestamp": "2023-11-01T10:02:30Z",
                "severity": "CRITICAL",
                "log_name": "auth-service-logs",
                "payload": {"message": "Authentication failed for multiple users", "attempted_users": ["baduser1", "baduser2"]}
            },
        ]

        summary = summarize_incident_logs(sample_incident_id, sample_error_logs)
        print(f"\nIncident Summary for {sample_incident_id}:\n{summary}")
