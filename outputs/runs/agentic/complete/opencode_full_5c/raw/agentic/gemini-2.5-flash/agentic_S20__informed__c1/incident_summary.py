import os
import google.generativeai as genai
from observability_models import LogQueryResult


def summarize_incident_with_gemini(error_logs: list[LogQueryResult]) -> str:
    """Summarizes error log findings for incident review using Google Gemini API."""
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    model = genai.GenerativeModel("gemini-pro")

    if not error_logs:
        return "No error logs provided for summary."

    log_texts = []
    for log in error_logs:
        log_texts.append(
            f"Timestamp: {log.timestamp}, Severity: {log.severity}, Message: {log.message}, Payload: {log.json_payload}"
        )

    prompt = (
        "The following are recent error logs. Please summarize the key issues, "
        "potential root causes, and suggest immediate actions for an incident responder. "
        "Focus on patterns, frequency, and critical details."
        "\n\n" + "\n".join(log_texts)
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary with Gemini API: {e}"


if __name__ == "__main__":
    # Example usage: Create some mock error logs
    mock_error_logs = [
        LogQueryResult(
            {
                "severity": "ERROR",
                "textPayload": "Database connection failed: Timeout",
                "timestamp": "2023-10-27T10:00:00Z",
            }
        ),
        LogQueryResult(
            {
                "severity": "ERROR",
                "jsonPayload": {
                    "message": "Service A unavailable",
                    "service": "ServiceA",
                },
                "timestamp": "2023-10-27T10:01:00Z",
            }
        ),
        LogQueryResult(
            {
                "severity": "CRITICAL",
                "textPayload": "Fatal error in payment gateway",
                "timestamp": "2023-10-27T10:05:00Z",
            }
        ),
        LogQueryResult(
            {
                "severity": "ERROR",
                "textPayload": "Database connection failed: Authentication error",
                "timestamp": "2023-10-27T10:06:00Z",
            }
        ),
    ]

    # In a real scenario, you would fetch these logs using query_error_logs.py
    # from query_error_logs import query_error_logs
    # fetched_logs = query_error_logs("your-log-name", min_severity="ERROR", time_range_minutes=30)

    summary = summarize_incident_with_gemini(mock_error_logs)
    print("\nIncident Summary:\n")
    print(summary)
