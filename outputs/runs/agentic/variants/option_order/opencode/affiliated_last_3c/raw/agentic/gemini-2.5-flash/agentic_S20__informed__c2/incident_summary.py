import os
import google.generativeai as genai
from observability_models import LogQueryResult


def summarize_incident_logs(log_results: LogQueryResult) -> str:
    """Summarizes error log findings for incident review using Google Gemini API."""
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using gemini-pro for text summarization

    if not log_results.entries:
        return "No log entries provided for summarization."

    log_text = "\n".join([str(entry) for entry in log_results.entries])

    prompt = (
        "Summarize the following error log entries into a concise incident report. "
        "Highlight key issues, affected components, and potential root causes. "
        "\n\nLog Entries:\n" + log_text
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing logs with Gemini API: {e}"


if __name__ == "__main__":
    # Example usage (assuming you have some error logs from query_error_logs.py)
    from query_error_logs import query_error_logs

    # In a real scenario, you'd call query_error_logs and pass its result here
    # For demonstration, let's create a dummy LogQueryResult
    dummy_entries = [
        {
            "severity": "ERROR",
            "message": "Failed to connect to database",
            "timestamp": "2023-10-27T10:00:00Z",
            "resource": {"type": "compute.googleapis.com/Instance"},
        },
        {
            "severity": "ERROR",
            "message": "Service Unavailable: User microservice",
            "timestamp": "2023-10-27T10:01:00Z",
            "jsonPayload": {"service": "user-service", "status": "503"},
        },
        {
            "severity": "WARNING",
            "message": "High CPU usage detected",
            "timestamp": "2023-10-27T09:55:00Z",
        },
    ]
    dummy_log_results = LogQueryResult(dummy_entries)

    print("\n--- Incident Summary ---")
    summary = summarize_incident_logs(dummy_log_results)
    print(summary)
