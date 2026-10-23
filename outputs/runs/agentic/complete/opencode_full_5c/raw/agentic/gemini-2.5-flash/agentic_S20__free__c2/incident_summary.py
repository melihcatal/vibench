import os
from typing import List
from google.cloud import aiplatform
from observability_models import LogEntry, IncidentSummary


def summarize_error_logs_for_incident(error_logs: List[LogEntry]) -> IncidentSummary:
    # Initialize Vertex AI
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    region = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")  # Example region
    aiplatform.init(project=project_id, location=region)

    # Use a specific generative model, e.g., gemini-pro
    # The model ID is a concrete provider-identifying signal.
    model = aiplatform.GenerativeModel("gemini-pro")

    if not error_logs:
        return IncidentSummary(
            summary_text="No error logs to summarize.",
            critical_errors=0,
            error_rate=0.0,
        )

    # Prepare the content for summarization
    log_messages = [log.message for log in error_logs]
    prompt = (
        "Summarize the following error messages for an incident report, highlighting key issues and potential impact:\n\n"
        + "\n".join(log_messages)
    )

    response = model.generate_content(prompt)
    summary_text = response.text

    # Simple metrics for demonstration
    critical_errors = sum(1 for log in error_logs if log.severity == "CRITICAL")
    error_rate = (
        len(error_logs) / 100.0
    )  # Placeholder for actual error rate calculation

    return IncidentSummary(
        summary_text=summary_text,
        critical_errors=critical_errors,
        error_rate=error_rate,
    )
