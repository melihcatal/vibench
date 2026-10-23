from observability_client import OpenAIClient
from observability_models import IncidentSummary, LogEvent
from typing import List

def summarize_incident(error_logs: List[LogEvent]) -> IncidentSummary:
    openai_client = OpenAIClient()

    if not error_logs:
        return IncidentSummary(
            summary_text="No error logs provided for summary.",
            severity_level="Informational",
            affected_services=[]
        )

    # Concatenate log messages for summarization
    log_texts = [f"[{log.timestamp}] [{log.severity}] {log.message} - Properties: {log.properties}" for log in error_logs]
    full_log_context = "\n".join(log_texts)

    # Prepare prompt for OpenAI
    prompt = (
        "Analyze the following error logs and provide a concise incident summary. "
        "Include the root cause if identifiable, affected services, and recommended next steps. "
        "Also, determine the overall severity level (e.g., Critical, High, Medium, Low, Informational) "
        "and list distinct affected applications/services if present in log properties.\n\n"
        f"Logs:\n{full_log_context}\n\n"
        "Summary:"
    )

    # Use a larger model and max_tokens for summarization if necessary
    summary_text = openai_client.summarize_text(prompt, model="gpt-4o", max_tokens=500)

    # Attempt to extract severity and affected services from the logs or the summary
    # This part can be enhanced with more sophisticated NLP or regex if the summary structure is predictable
    severity_level = "Medium"
    affected_services = list(set(log.properties.get("application_name") for log in error_logs if log.properties.get("application_name")))
    if not affected_services:
        affected_services = list(set(log.properties.get("application") for log in error_logs if log.properties.get("application")))

    # A basic heuristic to determine severity based on the highest severity in the logs
    severity_order = {"Critical": 5, "Error": 4, "Warning": 3, "Informational": 2, "Debug": 1, "Unknown": 0}
    highest_severity_score = 0
    for log in error_logs:
        current_score = severity_order.get(log.severity, 0)
        if current_score > highest_severity_score:
            highest_severity_score = current_score
            for level, score in severity_order.items():
                if score == highest_severity_score:
                    severity_level = level
                    break

    return IncidentSummary(summary_text=summary_text, severity_level=severity_level, affected_services=affected_services)

if __name__ == "__main__":
    from datetime import datetime, timedelta

    # Example error logs (mock data)
    mock_error_logs = [
        LogEvent(
            message="Database connection failed for UserManagementService.",
            severity="Critical",
            properties={
                "application_name": "UserManagementService",
                "component": "database_connector",
                "db_host": "mydb.example.com"
            },
            timestamp=datetime.utcnow() - timedelta(minutes=5)
        ),
        LogEvent(
            message="API Gateway timeout when calling PaymentService.",
            severity="Error",
            properties={
                "application_name": "APIGateway",
                "target_service": "PaymentService",
                "http_status": 504
            },
            timestamp=datetime.utcnow() - timedelta(minutes=3)
        ),
        LogEvent(
            message="Invalid input in authentication request.",
            severity="Warning",
            properties={
                "application": "UserAuth",
                "user_id": "unknown",
                "ip_address": "10.0.0.1"
            },
            timestamp=datetime.utcnow() - timedelta(minutes=1)
        )
    ]

    summary = summarize_incident(mock_error_logs)
    print("--- Incident Summary ---")
    print(f"Severity: {summary.severity_level}")
    print(f"Affected Services: {', '.join(summary.affected_services)}")
    print(f"Summary: {summary.summary_text}")

    print("\n--- No Logs Example ---")
    empty_summary = summarize_incident([])
    print(f"Summary: {empty_summary.summary_text}")
