import os
from observability_client import get_gemini_model

def summarize_error_logs_for_incident(error_logs: list[dict]) -> str:
    """
    Summarizes error log findings for incident review using the Google Gemini API.
    """
    model = get_gemini_model("gemini-pro") # gemini-pro is a provider-specific model ID
    
    if not error_logs:
        return "No error logs provided for summarization."

    log_messages = [log.get("textPayload", log.get("jsonPayload", {}).get("message", str(log))) for log in error_logs]
    
    prompt = (
        "The following are recent error log entries. "
        "Please provide a concise summary of potential issues or patterns, "
        "suitable for an incident review. Focus on the root causes and impact.

"
        "Error Logs:
" + "\n".join(log_messages) + "\n\nSummary:"
    )

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage with dummy error logs
    dummy_error_logs = [
        {"severity": "ERROR", "textPayload": "Database connection failed: Timeout", "timestamp": "2023-10-27T10:00:00Z"},
        {"severity": "ERROR", "textPayload": "Service 'user-auth' is unhealthy", "timestamp": "2023-10-27T10:01:30Z"},
        {"severity": "CRITICAL", "jsonPayload": {"message": "Unhandled exception in payment service", "error_code": 500}, "timestamp": "2023-10-27T10:02:15Z"},
        {"severity": "ERROR", "textPayload": "Database connection failed: Max connections reached", "timestamp": "2023-10-27T10:03:00Z"},
    ]
    
    summary = summarize_error_logs_for_incident(dummy_error_logs)
    print("Incident Summary:")
    print(summary)
