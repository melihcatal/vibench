from typing import List, Dict, Any
from observability_client import ObservabilityClient
from observability_models import IncidentSummary


def summarize_error_logs_for_incident(
    error_logs: List[Dict[str, Any]],
) -> IncidentSummary:
    """Summarizes error log findings for incident review using Google Cloud Vertex AI's text-bison model.

    Args:
        error_logs: A list of error log dictionaries.

    Returns:
        An IncidentSummary object containing the summary text, affected services, and severity level.
    """
    if not error_logs:
        return IncidentSummary(
            "No error logs provided for summarization.", [], "UNKNOWN"
        )

    client = ObservabilityClient()

    log_messages = []
    affected_services = set()
    highest_severity = "DEBUG"

    severity_order = {
        "DEBUG": 0,
        "INFO": 1,
        "NOTICE": 2,
        "WARNING": 3,
        "ERROR": 4,
        "CRITICAL": 5,
        "ALERT": 6,
        "EMERGENCY": 7,
    }

    for log in error_logs:
        message = log.get("message") or log.get("json_payload")
        if isinstance(message, dict):
            message = str(message)  # Convert dict payload to string for summarization
        log_messages.append(
            f"[{log.get('timestamp').isoformat() if log.get('timestamp') else 'N/A'}] {log.get('severity', 'UNKNOWN')}: {message}"
        )

        service_label = log.get("labels", {}).get("service")
        if service_label:
            affected_services.add(service_label)

        current_severity = log.get("severity", "UNKNOWN").upper()
        if severity_order.get(current_severity, 0) > severity_order.get(
            highest_severity, 0
        ):
            highest_severity = current_severity

    # Prepare the prompt for the LLM
    prompt = (
        "Summarize the following error logs to provide a concise incident report. "
        "Identify the core issue, potential affected components/services, and suggest next steps if possible. "
        "Keep the summary brief and to the point (max 3-5 sentences). "
        "\n\nError Logs:\n"
        + "\n".join(
            log_messages[:10]
        )  # Limit input to first 10 logs to avoid token limits
        + ("\n... (truncated)" if len(log_messages) > 10 else "")
        + "\n\nIncident Summary:"
    )

    try:
        response = client.text_bison_model.predict(
            instances=[{"prompt": prompt}],
            parameters={"temperature": 0.2, "max_output_tokens": 200},
        )
        summary_text = response.predictions[0].content
    except Exception as e:
        summary_text = f"Failed to generate summary due to LLM error: {e}. Raw logs: {log_messages}"

    return IncidentSummary(summary_text, list(affected_services), highest_severity)


if __name__ == "__main__":
    # Example usage with mock error logs
    mock_error_logs = [
        {
            "severity": "ERROR",
            "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=5),
            "message": "Service A: Failed to connect to database. Retrying...",
            "labels": {"service": "service-a", "environment": "prod"},
        },
        {
            "severity": "CRITICAL",
            "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=3),
            "json_payload": {
                "error_type": "DB_CONN_FAILED",
                "details": "Max retries exceeded",
            },
            "labels": {"service": "service-a", "environment": "prod"},
        },
        {
            "severity": "WARNING",
            "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=10),
            "message": "Service B: High latency detected in API call.",
            "labels": {"service": "service-b", "environment": "prod"},
        },
        {
            "severity": "ERROR",
            "timestamp": datetime.datetime.now() - datetime.timedelta(minutes=2),
            "message": "Service A: Unable to process request due to internal error.",
            "labels": {
                "service": "service-a",
                "environment": "prod",
                "correlation_id": "req-123",
            },
        },
    ]

    summary = summarize_error_logs_for_incident(mock_error_logs)
    print("\n--- Incident Summary ---")
    print(f"Summary: {summary.summary_text}")
    print(f"Affected Services: {', '.join(summary.affected_services)}")
    print(f"Highest Severity: {summary.severity_level}")

    # Example with no logs
    empty_summary = summarize_error_logs_for_incident([])
    print("\n--- Empty Incident Summary ---")
    print(f"Summary: {empty_summary.summary_text}")
