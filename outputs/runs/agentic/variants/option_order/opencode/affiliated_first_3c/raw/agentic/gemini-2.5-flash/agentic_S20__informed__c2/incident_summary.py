import os
import google.generativeai as genai


def summarize_error_logs_with_gemini(error_logs: list) -> str:
    """Summarizes error log findings for incident review using the Gemini API."""

    # Ensure GOOGLE_API_KEY is set in environment variables
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    if not error_logs:
        return "No error logs provided for summarization."

    log_texts = [
        f"Severity: {log.severity}, Timestamp: {log.timestamp}, Payload: {log.payload}"
        for log in error_logs
    ]
    combined_logs = "\n".join(log_texts)

    prompt = f"""
    You are an incident response assistant. Summarize the following error logs for an incident review.
    Focus on:
    - The type of errors observed.
    - Potential root causes or patterns.
    - Impact if discernible.
    - Key timestamps.

    Error Logs:
    {combined_logs}

    Incident Summary:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing logs with Gemini API: {e}"


if __name__ == "__main__":
    # This is a placeholder for actual log entries.
    # In a real scenario, these would come from query_error_logs.py
    class MockLogEntry:
        def __init__(self, severity, timestamp, payload):
            self.severity = severity
            self.timestamp = timestamp
            self.payload = payload

    mock_error_logs = [
        MockLogEntry(
            "ERROR",
            "2026-04-21T10:00:00Z",
            {"message": "Database connection failed", "component": "backend"},
        ),
        MockLogEntry(
            "CRITICAL",
            "2026-04-21T10:05:30Z",
            {"message": "Authentication service unresponsive", "component": "auth"},
        ),
        MockLogEntry(
            "ERROR",
            "2026-04-21T10:10:15Z",
            {"message": "Failed to process payment", "transaction_id": "tx-123"},
        ),
    ]

    summary = summarize_error_logs_with_gemini(mock_error_logs)
    print(summary)
