import os
import google.generativeai as genai

# Configure the Google Gemini API client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Ensure GOOGLE_API_KEY is set


def summarize_incident(error_logs: list[dict]) -> str:
    """
    Summarizes error log findings for incident review using the Gemini API.
    """
    if not error_logs:
        return "No error logs provided for summarization."

    log_strings = []
    for log in error_logs:
        log_strings.append(
            f"[{log.get('timestamp', 'N/A')}] {log.get('severity', 'N/A')}: "
            f"{log.get('message', 'N/A')} (Component: {log.get('component', 'N/A')})"
        )

    # Use a specific Gemini model, e.g., 'gemini-pro' for text tasks
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        "Summarize the following error logs into a concise incident report. "
        "Highlight the most critical errors, their potential causes, and affected components.\n\n"
        + "\n".join(log_strings)
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing incident: {e}"


if __name__ == "__main__":
    # Example usage (mock error logs)
    mock_errors = [
        {
            "timestamp": "2023-10-27T10:00:00Z",
            "severity": "ERROR",
            "message": "Database connection failed",
            "component": "data-service",
        },
        {
            "timestamp": "2023-10-27T10:01:15Z",
            "severity": "CRITICAL",
            "message": "Service 'user-auth' unresponsive",
            "component": "api-gateway",
        },
        {
            "timestamp": "2023-10-27T10:02:30Z",
            "severity": "ERROR",
            "message": "Invalid input parameter for user creation",
            "component": "user-service",
        },
    ]

    summary = summarize_incident(mock_errors)
    print(summary)
