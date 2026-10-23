import os
from datetime import datetime, timedelta
from google.cloud import logging
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from observability_client import ObservabilityClient
from observability_models import IncidentSummaryRequest

# Ensure GOOGLE_CLOUD_PROJECT environment variable is set
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

# Configure Generative AI - requires GOOGLE_API_KEY or gcloud auth
genai.configure(project=PROJECT_ID)

logging_client = ObservabilityClient(project_id=PROJECT_ID)


def summarize_error_logs_for_incident(request: IncidentSummaryRequest) -> str:
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(seconds=request.time_range_seconds)

    filter_string = (
        f'logName="projects/{request.project_id}/logs/{request.log_name}" '
        f'severity=("ERROR" OR "CRITICAL" OR "ALERT" OR "EMERGENCY") '
        f'timestamp>="{start_time.isoformat(timespec="seconds")}Z" '
        f'timestamp<="{end_time.isoformat(timespec="seconds")}Z"'
    )

    print(f"Fetching error logs for incident summary with filter: {filter_string}")

    error_logs = logging_client.query_logs(
        filter_string=filter_string,
        order_by="timestamp desc",
        limit=20,  # Limit logs for summarization to avoid large prompts
    )

    log_messages = []
    for entry in error_logs:
        if entry.payload:
            if isinstance(entry.payload, dict):
                message = entry.payload.get("message", str(entry.payload))
            else:
                message = str(entry.payload)
            log_messages.append(
                f"[{{entry.timestamp}}] [{{entry.severity}}] {{message}}"
            )

    if not log_messages:
        return "No error logs found to summarize for the given criteria."

    combined_logs = "\n".join(log_messages)

    # Use a generative AI model to summarize the logs
    try:
        model = genai.GenerativeModel(
            "gemini-1.0-pro"
        )  # Using a capable model for summarization
        prompt = f"Summarize the following error logs for an incident review. Focus on key issues, frequency, and potential impact:\n\n{{combined_logs}}"

        # Add safety settings to prevent harmful content generation
        response = model.generate_content(
            prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
        )
        return response.text
    except Exception as e:
        return f"Failed to summarize logs using Generative AI: {e}"


if __name__ == "__main__":
    # Example usage:
    summary_request = IncidentSummaryRequest(
        project_id=PROJECT_ID,
        log_name="my-structured-app-log",  # Or "my-correlated-app-log"
        time_range_seconds=3600,  # Last 1 hour
    )
    summary = summarize_error_logs_for_incident(summary_request)
    print("\n--- Incident Summary ---")
    print(summary)
