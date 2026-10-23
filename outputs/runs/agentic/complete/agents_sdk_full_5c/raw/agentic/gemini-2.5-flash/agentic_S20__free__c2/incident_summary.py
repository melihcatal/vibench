import os
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from observability_models import LogEntry, IncidentSummaryRequest, IncidentSummaryResponse

def summarize_error_logs_for_incident(request: IncidentSummaryRequest) -> IncidentSummaryResponse:
    """Summarizes error log findings for incident review using Vertex AI's PaLM 2 for Text."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GCP_REGION", "us-central1") # Choose an appropriate region for Vertex AI
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison")

    # Format log entries into a readable string for the LLM
    log_strings = []
    for log in request.error_logs:
        payload_str = str(log.json_payload) if log.json_payload else log.text_payload
        log_strings.append(
            f"Timestamp: {log.timestamp.isoformat()}, Severity: {log.severity}, "
            f"LogName: {log.log_name}, Message: {log.message}, Payload: {payload_str}"
        )
    
    log_block = "\n".join(log_strings)

    prompt = f"""
    Analyze the following error log entries and provide a concise incident summary.
    Identify the main issue, potential affected systems, and suggest immediate action items.
    
    {request.context if request.context else ""}
    
    Error Logs:
    {log_block}
    
    Please provide:
    1. A summary of the incident.
    2. A list of potential action items to investigate or mitigate.
    """

    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 800,
        "top_p": 0.8,
        "top_k": 40
    }

    try:
        response = model.predict(prompt, **parameters)
        response_text = response.text

        summary_start = response_text.find("1. A summary of the incident.")
        actions_start = response_text.find("2. A list of potential action items")

        summary_text = ""
        action_items = []

        if summary_start != -1 and actions_start != -1:
            summary_text = response_text[summary_start:actions_start].replace("1. A summary of the incident.", "").strip()
            action_items_raw = response_text[actions_start:].replace("2. A list of potential action items to investigate or mitigate.", "").strip()
            action_items = [item.strip() for item in action_items_raw.split('\n- ') if item.strip() and item.strip().startswith('- ')]
            action_items = [item[2:].strip() for item in action_items_raw.split('\n') if item.strip().startswith('- ')]
        elif summary_start != -1:
            summary_text = response_text[summary_start:].replace("1. A summary of the incident.", "").strip()
        else:
            summary_text = response_text.strip() # Fallback if markers are not found
        
        return IncidentSummaryResponse(
            summary_text=summary_text,
            action_items=action_items
        )
    except Exception as e:
        print(f"Error generating incident summary: {e}")
        return IncidentSummaryResponse(
            summary_text=f"Failed to generate summary due to an error: {e}",
            action_items=["Review raw logs manually.", "Check Vertex AI service status."]
        )

if __name__ == "__main__":
    # This is a simplified example. In a real scenario, you'd fetch actual error logs.
    from datetime import datetime, timezone
    
    # Mock log entries for demonstration
    mock_error_logs = [
        LogEntry(
            timestamp=datetime.now(timezone.utc),
            severity="ERROR",
            message="Database connection pool exhausted.",
            log_name="my-app-logs",
            resource_type="global",
            json_payload={"component": "data-access", "error_code": "DB-001"}
        ),
        LogEntry(
            timestamp=datetime.now(timezone.utc),
            severity="CRITICAL",
            message="Service 'payment-gateway' failed to start.",
            log_name="my-app-logs",
            resource_type="global",
            json_payload={"component": "startup", "service_name": "payment-gateway"}
        ),
        LogEntry(
            timestamp=datetime.now(timezone.utc),
            severity="ERROR",
            message="External API request timed out after 30s.",
            log_name="my-app-logs",
            resource_type="global",
            json_payload={"component": "payment-service", "api_url": "https://external.api/v1/process", "duration_ms": 30000}
        )
    ]

    request = IncidentSummaryRequest(
        error_logs=mock_error_logs,
        context="A recent deployment might be related to these errors."
    )

    try:
        summary_response = summarize_error_logs_for_incident(request)
        print("\n--- Incident Summary ---")
        print(f"Summary: {summary_response.summary_text}")
        print("\nAction Items:")
        for item in summary_response.action_items:
            print(f"- {item}")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure GOOGLE_CLOUD_PROJECT and GCP_REGION environment variables are set.")
