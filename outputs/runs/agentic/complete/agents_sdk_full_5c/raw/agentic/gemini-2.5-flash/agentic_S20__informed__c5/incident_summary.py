import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_error_logs(error_logs: List[Dict[str, Any]], model_name: str = "gemini-pro") -> str:
    """
    Summarizes error log findings for incident review using the Google Gemini API.
    """
    # Ensure GOOGLE_API_KEY environment variable is set
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)

    log_texts = [f"Severity: {log['severity']}, Message: {log['message']}, Timestamp: {log['timestamp']}" for log in error_logs]
    logs_input = "\n".join(log_texts)

    prompt = f"""
    Review the following error log entries and provide a concise summary for an incident review.
    Identify potential root causes, affected components, and suggest immediate next steps if possible.

    Error Log Entries:
    '''
    {logs_input}
    '''

    Incident Summary:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_API_KEY environment variable before running
    sample_error_logs = [
        {
            "severity": "ERROR",
            "message": "Database connection failed for user_service.",
            "timestamp": "2023-10-27T10:00:00Z",
            "component": "user_service",
            "error_code": "DB-001"
        },
        {
            "severity": "ERROR",
            "message": "Authentication service timed out when validating token.",
            "timestamp": "2023-10-27T10:01:15Z",
            "component": "auth_service",
            "error_code": "AUTH-504"
        },
        {
            "severity": "CRITICAL",
            "message": "Out of memory in payment_processor.",
            "timestamp": "2023-10-27T10:02:30Z",
            "component": "payment_processor",
            "error_code": "OOM-001"
        },
    ]

    summary = summarize_error_logs(sample_error_logs)
    print("\n--- Incident Summary ---")
    print(summary)
