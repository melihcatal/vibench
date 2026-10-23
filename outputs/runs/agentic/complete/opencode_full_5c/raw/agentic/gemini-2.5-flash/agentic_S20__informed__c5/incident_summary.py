from observability_client import get_gemini_model
from typing import List, Dict, Any


def summarize_error_logs(error_logs: List[Dict[str, Any]]) -> str:
    """Summarizes error log findings for incident review using the Gemini API."""
    model = get_gemini_model()

    if not error_logs:
        return "No error logs provided for summary."

    log_texts = []
    for log in error_logs:
        # Attempt to extract a meaningful log message
        message = (
            log.get("textPayload")
            or log.get("jsonPayload", {}).get("message")
            or str(log)
        )
        log_texts.append(
            f"[{log.get('severity', 'UNKNOWN')}] {log.get('timestamp', '')}: {message}"
        )

    combined_logs = "\n".join(log_texts)

    prompt = f"""Review the following error logs and provide a concise incident summary. Highlight the key issues, potential root causes, and any recurring patterns. Limit the summary to 3-5 bullet points. If no errors, indicate that. Avoid disclaimers. Do not include a conversational opening or closing, just the summary. Format the output as bullet points. 

Error Logs:
{combined_logs}
"""

    print("Sending request to Gemini API for incident summary...")
    try:
        response = model.generate_content(prompt)
        if response and response.candidates:
            summary = response.candidates[0].content.parts[0].text
            print("Incident summary generated successfully.")
            return summary
        else:
            return "Failed to generate incident summary: No candidates found."
    except Exception as e:
        return f"Failed to generate incident summary: {str(e)}"


if __name__ == "__main__":
    # Example usage (mock error logs):
    mock_error_logs = [
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:00:00Z",
            "jsonPayload": {
                "message": "Database connection timed out",
                "service": "user-service",
            },
        },
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:01:30Z",
            "jsonPayload": {
                "message": "Failed to write to cache",
                "cache_key": "session_123",
            },
        },
        {
            "severity": "CRITICAL",
            "timestamp": "2023-10-27T10:02:15Z",
            "textPayload": "Service 'payment-gateway' is unresponsive, health check failed.",
        },
        {
            "severity": "ERROR",
            "timestamp": "2023-10-27T10:03:00Z",
            "jsonPayload": {
                "message": "Database connection timed out",
                "service": "product-service",
            },
        },
    ]

    summary = summarize_error_logs(mock_error_logs)
    print("\n--- Incident Summary ---")
    print(summary)

    # Example with no errors
    no_error_logs = []
    summary_no_errors = summarize_error_logs(no_error_logs)
    print("\n--- Incident Summary (No Errors) ---")
    print(summary_no_errors)
