from typing import List
from observability_models import LogEntryResponse
from google.cloud import aiplatform
import os


def summarize_error_logs_for_incident(
    error_logs: List[LogEntryResponse],
    project_id: str = None,
    location: str = "us-central1",
) -> str:
    """Summarizes a list of error log entries for incident review using Google Cloud Vertex AI (Gemini Pro).

    Args:
        error_logs: A list of LogEntryResponse objects containing error logs.
        project_id: The GCP project ID. If None, it will be inferred from the environment.
        location: The GCP region for Vertex AI. Default is 'us-central1'.

    Returns:
        A string containing the incident summary.
    """
    if not error_logs:
        return "No error logs provided for summary."

    if not project_id:
        project_id = os.getenv("GCP_PROJECT_ID")
        if not project_id:
            raise ValueError(
                "GCP_PROJECT_ID environment variable or project_id argument must be set."
            )

    # Initialize Vertex AI - Provider-identifying signal: aiplatform.init
    aiplatform.init(project=project_id, location=location)

    # Load the model - Provider-identifying signal: gemini-pro model ID
    # The SDK client is also a provider-identifying signal
    model = aiplatform.GenerativeModel("gemini-pro")

    log_messages = [
        f"[{log.timestamp}] {log.severity}: {log.message}" for log in error_logs
    ]
    logs_text = "\n".join(log_messages)

    prompt = f"""Review the following error logs and provide a concise incident summary. Highlight key issues, potential root causes if apparent, and any recurring patterns. Limit the summary to 200 words.

    Error Logs:
    {logs_text}

    Incident Summary:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing logs with Vertex AI: {e}")
        return f"Failed to generate incident summary. Error: {str(e)}"


if __name__ == "__main__":
    # Example Usage (requires GCP_PROJECT_ID env var and Vertex AI enabled)
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print("Please set the GCP_PROJECT_ID environment variable to run this example.")
    else:
        # Create some dummy error logs for demonstration
        from datetime import datetime, timedelta

        dummy_error_logs = [
            LogEntryResponse(
                timestamp=datetime.utcnow() - timedelta(minutes=5),
                severity="ERROR",
                message="Service A: Database connection timed out. Host: db-prod-01",
                resource_type="gce_instance",
                resource_labels={"instance_id": "vm-1"},
                labels={},
                insert_id="1",
                log_name="app-error",
            ),
            LogEntryResponse(
                timestamp=datetime.utcnow() - timedelta(minutes=3),
                severity="CRITICAL",
                message="Service B: Unhandled exception in /api/v1/process. NullPointerException.",
                resource_type="k8s_container",
                resource_labels={"pod_name": "pod-xyz"},
                labels={},
                insert_id="2",
                log_name="app-error",
            ),
            LogEntryResponse(
                timestamp=datetime.utcnow() - timedelta(minutes=2),
                severity="ERROR",
                message="Service A: Failed to write to cache. Redis unreachable.",
                resource_type="gce_instance",
                resource_labels={"instance_id": "vm-1"},
                labels={},
                insert_id="3",
                log_name="app-error",
            ),
        ]

        summary = summarize_error_logs_for_incident(
            dummy_error_logs, project_id=project_id
        )
        print("\n--- Incident Summary ---")
        print(summary)
