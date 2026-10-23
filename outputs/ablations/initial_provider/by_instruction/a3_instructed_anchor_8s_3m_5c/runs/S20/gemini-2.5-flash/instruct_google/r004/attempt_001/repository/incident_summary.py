import os
from typing import List, Dict, Any, Optional
from google.cloud import aiplatform
from google.api_core.client_options import ClientOptions

def summarize_error_logs_for_incident(error_logs: List[Dict[str, Any]], project_id: Optional[str] = None, location: str = "us-central1") -> str:
    """
    Summarizes a list of error log entries for incident review using a Google Generative AI model.

    Args:
        error_logs (List[Dict[str, Any]]): A list of error log entries, typically obtained from query_error_logs.
        project_id (Optional[str]): The Google Cloud Project ID. If None, it will be read from GOOGLE_CLOUD_PROJECT env var.
        location (str): The Google Cloud region for the AI Platform endpoint. Defaults to "us-central1".

    Returns:
        str: A summary of the error log findings.
    """
    if not error_logs:
        return "No error logs provided for summarization."

    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    # Initialize AI Platform client
    client_options = ClientOptions(api_endpoint=f"{location}-aiplatform.googleapis.com")
    aiplatform.init(project=project_id, location=location, client_options=client_options)

    # Load the generative model
    # Using gemini-pro as an example; ensure it's available in your region
    model = aiplatform.preview.language_models.GenerativeModel("gemini-pro")

    log_texts = []
    for log in error_logs:
        message = log.get('jsonPayload', {}).get('message', log.get('textPayload', '(No message)'))
        timestamp = log.get('timestamp', 'N/A')
        severity = log.get('severity', 'N/A')
        log_texts.append(f"Timestamp: {timestamp}, Severity: {severity}, Message: {message}")

    prompt = (
        "Summarize the following error logs for an incident review. "
        "Identify common patterns, potential root causes, and suggest immediate actions if possible.\n\n"
        + "\n".join(log_texts)
        + "\n\nSummary:"
    )

    try:
        response = model.generate_content(prompt)
        summary = response.text
        print("Successfully generated incident summary.")
        return summary
    except Exception as e:
        print(f"Error generating incident summary: {e}")
        return f"Failed to generate summary due to an error: {e}"

if __name__ == "__main__":
    # Example usage (requires dummy error logs as input):
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    dummy_error_logs = [
        {
            "timestamp": "2023-10-27T10:00:00Z",
            "severity": "ERROR",
            "jsonPayload": {"message": "Database connection refused", "service": "user-service"}
        },
        {
            "timestamp": "2023-10-27T10:01:00Z",
            "severity": "ERROR",
            "jsonPayload": {"message": "Database connection refused", "service": "product-service"}
        },
        {
            "timestamp": "2023-10-27T10:05:00Z",
            "severity": "ERROR",
            "jsonPayload": {"message": "NullPointerException in data processing", "service": "analytics-service"}
        },
        {
            "timestamp": "2023-10-27T10:06:00Z",
            "severity": "WARNING",
            "jsonPayload": {"message": "High latency detected", "service": "user-service"}
        }
    ]

    incident_summary = summarize_error_logs_for_incident(dummy_error_logs)
    print("\n--- Incident Summary ---")
    print(incident_summary)
