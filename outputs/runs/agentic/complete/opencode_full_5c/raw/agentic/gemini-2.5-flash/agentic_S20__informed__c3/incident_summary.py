import google.generativeai as genai
import os


def summarize_incident(error_logs):
    """Summarizes error-log findings for incident review using the Google Gemini API.

    Args:
        error_logs (list): A list of dictionaries, where each dictionary represents an error log entry.

    Returns:
        str: A summary of the incident based on the error logs.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        return "Error: GOOGLE_API_KEY environment variable not set."

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-pro")  # Using a suitable Gemini model

    if not error_logs:
        return "No error logs provided for summarization."

    log_texts = []
    for log in error_logs:
        log_texts.append(
            f"Severity: {log.get('severity', 'UNKNOWN')}, Message: {log.get('message', 'N/A')}, Timestamp: {log.get('timestamp', 'N/A')}, Details: {log}"
        )

    prompt = (
        "Review the following error log entries and provide a concise summary for an incident review. "
        "Identify key issues, potential root causes, and affected components or users. "
        "Organize the summary into bullet points. Focus on actionable insights."
        "\n\n" + "\n".join(log_texts)
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary from Gemini API: {e}"


if __name__ == "__main__":
    # Example usage with dummy error logs
    example_error_logs = [
        {
            "timestamp": "2023-10-27T10:00:00Z",
            "severity": "ERROR",
            "message": "Database connection refused",
            "component": "auth-service",
            "database": "users_db",
        },
        {
            "timestamp": "2023-10-27T10:01:15Z",
            "severity": "ERROR",
            "message": "NullPointerException in user registration",
            "component": "user-service",
            "user_id": "temp-user",
        },
        {
            "timestamp": "2023-10-27T10:02:30Z",
            "severity": "CRITICAL",
            "message": "Payment gateway unresponsive",
            "component": "payment-service",
        },
    ]

    summary = summarize_incident(example_error_logs)
    print("\n--- Incident Summary ---")
    print(summary)
