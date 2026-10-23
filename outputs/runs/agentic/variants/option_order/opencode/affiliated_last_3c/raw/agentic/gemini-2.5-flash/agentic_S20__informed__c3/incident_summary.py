import os
import google.generativeai as genai


def summarize_incident_logs(error_logs: list[dict]) -> str:
    # Configure the Gemini API client
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for text generation

    if not error_logs:
        return "No error logs provided for incident summary."

    log_texts = []
    for log in error_logs:
        payload = log.get("json_payload") or {
            "message": log.get("text_payload", "")
        }  # Use text_payload if no json
        log_texts.append(
            f"Timestamp: {log.get('timestamp')}, Severity: {log.get('severity')}, Message: {payload}"
        )

    combined_logs = "\n".join(log_texts)

    prompt = f"""Review the following error logs and provide a concise incident summary. Highlight the key issues, potential causes, and any patterns observed. Max 200 words. 

Logs:
{combined_logs}

Incident Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"


if __name__ == "__main__":
    # Example usage with dummy error logs
    sample_error_logs = [
        {
            "timestamp": "2023-10-27T10:00:00Z",
            "severity": "ERROR",
            "json_payload": {
                "event": "database_connection_failed",
                "details": "Timeout connecting to DB server at 10.0.0.5",
            },
        },
        {
            "timestamp": "2023-10-27T10:01:15Z",
            "severity": "ERROR",
            "json_payload": {
                "event": "api_auth_failure",
                "user_id": "guest",
                "reason": "Invalid API key",
            },
        },
        {
            "timestamp": "2023-10-27T10:02:30Z",
            "severity": "WARNING",
            "text_payload": "High CPU usage detected on backend server",
        },
    ]

    summary = summarize_incident_logs(sample_error_logs)
    print("\n--- Incident Summary ---")
    print(summary)
