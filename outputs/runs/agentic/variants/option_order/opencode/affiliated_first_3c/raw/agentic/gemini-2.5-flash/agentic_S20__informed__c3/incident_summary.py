import google.generativeai as genai
import os


def summarize_incident_logs(error_logs_data):
    """
    Summarizes error-log findings for incident review using the Google Gemini API.
    `error_logs_data` is a list of dictionaries, where each dictionary represents an error log entry.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    log_texts = []
    for log in error_logs_data:
        log_texts.append(
            f"Timestamp: {log.get('timestamp')}, Severity: {log.get('severity')}, Message: {log.get('payload')}"
        )

    prompt = (
        "The following are error log entries. Please summarize the key issues, "
        "potential root causes, and any recurring patterns to assist in incident review. "
        "Provide a concise summary.\n\n" + "\n".join(log_texts)
    )

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_API_KEY environment variable is set.
    # sample_error_logs = [
    #     {"timestamp": "2023-10-27T10:00:00Z", "severity": "ERROR", "payload": "Database connection failed"},
    #     {"timestamp": "2023-10-27T10:01:00Z", "severity": "ERROR", "payload": "NullPointerException in user service"},
    #     {"timestamp": "2023-10-27T10:05:00Z", "severity": "ERROR", "payload": "Database connection failed"},
    #     {"timestamp": "2023-10-27T10:06:00Z", "severity": "WARNING", "payload": "High CPU usage detected"},
    # ]
    # summary = summarize_incident_logs(sample_error_logs)
    # print(summary)
    pass
