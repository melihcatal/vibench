import os
from google.cloud import aiplatform
from observability_models import IncidentSummaryRequest, IncidentSummaryResponse

def summarize_incident_logs(
    request: IncidentSummaryRequest,
    project_id: str = None,
    location: str = "us-central1",
    model_name: str = "gemini-pro"
) -> IncidentSummaryResponse:
    """Summarizes error log findings using Google Cloud Vertex AI (Generative AI)."""

    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("project_id must be provided or GOOGLE_CLOUD_PROJECT env var set.")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel(model_name)

    prompt_parts = [
        "You are an incident response assistant. Summarize the following error logs to identify the core issue, assess severity, and suggest immediate actions. Focus on brevity and clarity.",
        "",
        "Error Logs:",
        request.error_logs_text,
        "",
    ]

    if request.context_info:
        prompt_parts.append("Context:")
        prompt_parts.append(request.context_info)
        prompt_parts.append("")

    prompt_parts.append("Please provide:")
    prompt_parts.append("1. A concise summary of the problem.")
    prompt_parts.append("2. An assessment of the likely severity (e.g., Critical, High, Medium, Low).")
    prompt_parts.append("3. Up to three immediate action recommendations.")
    prompt_parts.append("")
    prompt_parts.append("Format your response clearly with these headings.")

    full_prompt = "\n".join(prompt_parts)
    
    print(f"Sending prompt to Vertex AI model {model_name} for incident summary...")
    try:
        response = model.generate_content(full_prompt)
        summary_content = response.text
        
        # Simple parsing of the generated text into the desired structured response
        summary_text = "No summary found."
        severity_assessment = "Unknown"
        action_recommendations = "No actions recommended."

        if "1. A concise summary of the problem." in summary_content:
            parts = summary_content.split("1. A concise summary of the problem.", 1)[1]
            summary_text = parts.split("2. An assessment of the likely severity", 1)[0].strip()
        
        if "2. An assessment of the likely severity" in summary_content:
            parts = summary_content.split("2. An assessment of the likely severity", 1)[1]
            severity_assessment = parts.split("3. Up to three immediate action recommendations.", 1)[0].strip()

        if "3. Up to three immediate action recommendations." in summary_content:
            action_recommendations = summary_content.split("3. Up to three immediate action recommendations.", 1)[1].strip()

        return IncidentSummaryResponse(
            summary_text=summary_text,
            severity_assessment=severity_assessment,
            action_recommendations=action_recommendations
        )

    except Exception as e:
        print(f"Error generating summary: {e}")
        return IncidentSummaryResponse(
            summary_text=f"Failed to generate summary due to error: {e}",
            severity_assessment="Critical",
            action_recommendations="Check AI service status and logs."
        )

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Ensure Vertex AI API is enabled and you have necessary permissions.
    
    sample_error_logs = """
    [2023-10-27 10:00:01 ERROR] Database connection timed out for 'user_service'.
    [2023-10-27 10:00:05 ERROR] Failed to fetch user data from DB. Service unavailable.
    [2023-10-27 10:00:10 WARN] High latency detected in 'auth_service'.
    [2023-10-27 10:00:15 ERROR] User authentication failed for multiple users.
    """

    request = IncidentSummaryRequest(
        error_logs_text=sample_error_logs,
        context_info="Application: User Management Service, Environment: Production, Region: Europe-west1"
    )

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        summary_response = summarize_incident_logs(request, project_id=project_id)
        print("\n--- Incident Summary ---")
        print(f"Summary: {summary_response.summary_text}")
        print(f"Severity: {summary_response.severity_assessment}")
        print(f"Actions: {summary_response.action_recommendations}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
