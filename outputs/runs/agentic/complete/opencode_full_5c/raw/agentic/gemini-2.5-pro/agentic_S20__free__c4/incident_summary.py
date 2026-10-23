import os
from typing import List
from observability_client import get_generative_model_client
from observability_models import IncidentSummaryRequest, IncidentSummaryResponse


def summarize_incident(request: IncidentSummaryRequest) -> IncidentSummaryResponse:
    """
    Summarizes error-log findings for incident review using Google's Gemini model.
    """
    if not request.error_logs:
        return IncidentSummaryResponse(summary="No error logs provided.")

    model = get_generative_model_client(model_name="gemini-1.5-flash-001")

    log_entries_str = "\n".join(request.error_logs)

    prompt = f"""
    The following are error logs from a recent incident. Please summarize them.
    Identify the most likely root cause, the timeline of events, and the key
    error messages. Structure the output clearly for an incident review meeting.

    Logs:
    {log_entries_str}
    """

    response = model.generate_content(prompt)

    summary = response.text
    return IncidentSummaryResponse(summary=summary)


if __name__ == "__main__":
    if os.environ.get("GCP_PROJECT_ID"):
        sample_errors = [
            "2023-10-27T10:00:00Z ERROR: Database connection failed: timeout expired",
            "2023-10-27T10:00:05Z ERROR: API endpoint /api/users returned 503 Service Unavailable",
            "2023-10-27T10:01:10Z ERROR: Failed to process payment for user-abc: Payment gateway timeout",
            "2023-10-27T10:01:15Z ERROR: Database connection failed: timeout expired",
        ]
        request = IncidentSummaryRequest(error_logs=sample_errors)
        result = summarize_incident(request)
        print("--- Incident Summary ---")
        print(result.summary)
    else:
        print("GCP_PROJECT_ID environment variable not set. Skipping example run.")
