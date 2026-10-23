import os
from typing import List, Dict, Any
from observability_client import get_gemini_model


def incident_summary(error_logs: List[Dict[str, Any]]) -> str:
    model = get_gemini_model()

    if not error_logs:
        return "No error logs provided for summarization."

    log_texts = []
    for log in error_logs:
        # Assuming log is a dict-like object from google.cloud.logging_v2.entries.LogEntry
        # Extracting relevant parts for summarization
        text = f"Severity: {log.get('severity', 'UNKNOWN')}, Timestamp: {log.get('timestamp', 'UNKNOWN')}, Payload: {log.get('payload', log.get('json_payload', ''))}"
        log_texts.append(text)

    prompt = (
        "Summarize the following error logs for an incident review. "
        "Identify key issues, frequency, and potential root causes. "
        "Provide a concise summary in bullet points.\n\n" + "\n".join(log_texts)
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"


if __name__ == "__main__":
    # This is a placeholder for demonstration. In a real scenario, you'd fetch actual error logs.
    sample_error_logs = [
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:00:00Z",
            "payload": "Database connection failed for user_id: 123. Error: Timeout",
        },
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:01:05Z",
            "payload": "Service 'auth-service' unavailable. Retrying...",
        },
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:02:10Z",
            "json_payload": {
                "error_code": 500,
                "message": "Unhandled exception in API /users",
                "user_id": "user-456",
            },
        },
    ]

    # Ensure GOOGLE_API_KEY is set in environment for this to run
    if "GOOGLE_API_KEY" not in os.environ:
        print("Please set the GOOGLE_API_KEY environment variable to run this example.")
    else:
        summary = incident_summary(sample_error_logs)
        print("Incident Summary:")
        print(summary)
