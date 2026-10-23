import google.generativeai as genai
import os
from observability_models import LogEntry

def summarize_incident(error_logs: list[LogEntry]) -> str:
    # Configure the Google Generative AI client
    # Ensure GOOGLE_API_KEY is set in your environment variables
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Use the Gemini Pro model
    model = genai.GenerativeModel('gemini-pro')

    if not error_logs:
        return "No error logs provided for incident summary."

    log_texts = []
    for log in error_logs:
        log_texts.append(f"Timestamp: {log.timestamp}, Severity: {log.severity}, Message: {log.message}")
    
    prompt = (
        "The following are recent error log entries. "
        "Please summarize the key issues, potential causes, and suggest immediate actions "
        "for an incident review. Focus on identifying patterns or critical events."
        "\n\n" + "\n".join(log_texts)
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating incident summary: {e}"

if __name__ == "__main__":
    # Example Usage (assuming you have some error logs, e.g., from query_error_logs)
    # In a real scenario, you would call query_error_logs to get actual data.
    sample_error_logs = [
        LogEntry(
            timestamp="2026-09-19T10:00:00Z",
            severity="ERROR",
            message="Database connection failed: Timeout connecting to primary replica.",
            resource_type="database",
            resource_labels={"db_name": "prod-db"}
        ),
        LogEntry(
            timestamp="2026-09-19T10:01:15Z",
            severity="ERROR",
            message="Application crashed due to unhandled exception in payment module.",
            resource_type="compute",
            resource_labels={"instance_id": "app-server-1"}
        ),
        LogEntry(
            timestamp="2026-09-19T10:02:30Z",
            severity="WARNING",
            message="High CPU utilization detected on app-server-2, near 95%.",
            resource_type="compute",
            resource_labels={"instance_id": "app-server-2"}
        ),
        LogEntry(
            timestamp="2026-09-19T10:05:00Z",
            severity="ERROR",
            message="Database connection failed: Too many open connections.",
            resource_type="database",
            resource_labels={"db_name": "prod-db"}
        ),
    ]

    summary = summarize_incident(sample_error_logs)
    print("\n--- Incident Summary ---")
    print(summary)
