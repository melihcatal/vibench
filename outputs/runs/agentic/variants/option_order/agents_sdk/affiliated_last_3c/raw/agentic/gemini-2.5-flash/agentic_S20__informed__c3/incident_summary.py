import os
import google.generativeai as genai

# Ensure GOOGLE_API_KEY is set as an environment variable
# export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"

def summarize_error_logs_for_incident(log_entries: list[dict]):
    """
    Summarizes a list of error log entries using the Google Gemini API for incident review.
    
    Args:
        log_entries: A list of dictionaries, where each dictionary represents a log entry.
    
    Returns:
        A string containing the summarized incident report.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    if not log_entries:
        return "No error logs provided for summarization."

    # Format log entries into a readable string for the LLM
    formatted_logs = []
    for i, entry in enumerate(log_entries):
        # Flatten jsonPayload for better readability for the LLM
        payload_str = ""
        if 'jsonPayload' in entry and isinstance(entry['jsonPayload'], dict):
            payload_items = [f"{k}: {v}" for k, v in entry['jsonPayload'].items()]
            payload_str = ", ".join(payload_items)
        elif 'textPayload' in entry:
            payload_str = entry['textPayload']
        
        formatted_logs.append(
            f"Log Entry {i+1} (Severity: {entry.get('severity', 'UNKNOWN')}, Timestamp: {entry.get('timestamp', 'UNKNOWN')}):
"
            f"  Message: {entry.get('message', 'N/A')}
"
            f"  Details: {payload_str}
"
        )
    
    logs_text = "\n".join(formatted_logs)

    prompt = (
        "You are an incident response assistant. Review the following error log entries and provide "
        "a concise summary for an incident report. Identify the core issue, potential impact, "
        "and any recurring patterns or key identifiers. Suggest next steps if possible.

"
        "--- START LOG ENTRIES ---
"
        f"{logs_text}
"
        "--- END LOG ENTRIES ---

"
        "Incident Summary:"
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == "__main__":
    # Example Usage:
    # This is a mock list of log entries. In a real scenario, these would come from query_error_logs.py
    example_error_logs = [
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:00:00Z",
            "message": "Database connection refused.",
            "jsonPayload": {
                "component": "data-access-layer",
                "database_host": "db-prod-1",
                "error_code": "DB-CONN-001",
                "user_id": "system"
            }
        },
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:01:15Z",
            "message": "Failed to write to cache.",
            "jsonPayload": {
                "component": "cache-service",
                "cache_key": "user_session_123",
                "reason": "Cache server unresponsive",
                "server": "cache-node-01"
            }
        },
        {
            "severity": "CRITICAL",
            "timestamp": "2023-10-27T10:02:30Z",
            "message": "Service 'user-auth' health check failed.",
            "jsonPayload": {
                "component": "health-monitor",
                "service_name": "user-auth",
                "endpoint": "/healthz",
                "status_code": 500
            }
        },
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:03:05Z",
            "message": "Database connection refused.",
            "jsonPayload": {
                "component": "data-access-layer",
                "database_host": "db-prod-1",
                "error_code": "DB-CONN-001",
                "user_id": "app-svc-2"
            }
        }
    ]

    print("Generating incident summary...")
    summary = summarize_error_logs_for_incident(example_error_logs)
    print("\n--- INCIDENT SUMMARY ---")
    print(summary)
    print("------------------------")

    print("\nGenerating summary for no logs...")
    no_logs_summary = summarize_error_logs_for_incident([])
    print(no_logs_summary)
