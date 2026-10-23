import os
from typing import Dict, Any
from observability_client import get_gemini_model
from observability_models import IncidentSummaryRequest

def summarize_incident_logs(request: IncidentSummaryRequest) -> str:
    """
    Summarizes error-log findings for incident review using the Gemini API.
    """
    model = get_gemini_model("gemini-pro") # Using gemini-pro for text generation

    if not request.error_logs:
        return "No error logs provided for summary."

    log_string = "\n".join([str(log) for log in request.error_logs])

    prompt = f"""Analyze the following error logs and provide a concise summary for an incident review. 
Focus on identifying the root cause, affected components, frequency, and any immediate actions needed.

Logs:
{log_string}

Context: {request.context if request.context else ""}

Incident Summary:"""

    print("Sending logs to Gemini for summarization...")
    response = model.generate_content(prompt)
    summary = response.text

    print("Gemini summary received.")
    return summary

if __name__ == "__main__":
    # Example usage
    # Set GOOGLE_API_KEY environment variable
    sample_error_logs = [
        {"timestamp": "2023-10-27T10:00:00Z", "severity": "ERROR", "message": "Database connection lost", "component": "backend-service"},
        {"timestamp": "2023-10-27T10:00:05Z", "severity": "ERROR", "message": "Failed to retrieve user data", "component": "user-auth-service", "user_id": "user-abc"},
        {"timestamp": "2023-10-27T10:00:10Z", "severity": "ERROR", "message": "Database connection lost", "component": "backend-service"},
        {"timestamp": "2023-10-27T10:00:15Z", "severity": "CRITICAL", "message": "Service unavailable", "component": "api-gateway"},
    ]

    incident_request = IncidentSummaryRequest(
        error_logs=sample_error_logs,
        context="Recent spikes in API errors during peak hours."
    )

    try:
        summary = summarize_incident_logs(incident_request)
        print("\n--- Incident Summary ---")
        print(summary)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
