import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_error_logs(error_logs: List[Dict[str, Any]]) -> str:
    """
    Summarizes a list of error log entries using the Google Gemini API.
    """
    if not error_logs:
        return "No error logs provided for summarization."

    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    if not genai.get_default_retriever(): # Check if a model is set for genai
        genai.set_default_model('gemini-pro') # Use a concrete model identifier

    model = genai.GenerativeModel('gemini-pro')

    log_strings = [
        f"Timestamp: {log.get('timestamp')}, Severity: {log.get('severity')}, Message: {log.get('payload', {}).get('message', log.get('payload'))}, Component: {log.get('payload', {}).get('component')}"
        for log in error_logs
    ]
    
    prompt = f"""
    Please summarize the following error logs to identify potential incidents, common patterns, or critical issues.
    Focus on the root causes and suggest immediate next steps if possible.

    Error Logs:
    {'
'.join(log_strings)}

    Summary:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing logs with Gemini API: {e}"

if __name__ == "__main__":
    # Example usage with mock error logs
    mock_error_logs = [
        {"timestamp": "2023-10-27T10:00:00Z", "severity": "ERROR", "payload": {"message": "Database connection failed", "component": "db-service"}},
        {"timestamp": "2023-10-27T10:01:00Z", "severity": "ERROR", "payload": {"message": "Service unavailable", "component": "api-gateway"}},
        {"timestamp": "2023-10-27T10:02:00Z", "severity": "ERROR", "payload": {"message": "Database connection failed", "component": "db-service"}},
        {"timestamp": "2023-10-27T10:03:00Z", "severity": "CRITICAL", "payload": {"message": "Disk usage critical on primary server", "component": "system-monitor"}}
    ]

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        summary = summarize_error_logs(mock_error_logs)
        print("Incident Summary:")
        print(summary)
