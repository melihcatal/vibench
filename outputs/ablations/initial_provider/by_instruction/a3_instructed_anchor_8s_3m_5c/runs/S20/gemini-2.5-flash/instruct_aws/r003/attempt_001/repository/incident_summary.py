import os
from google.cloud import aiplatform

def summarize_incident(log_entries: list[dict]) -> str:
    # Initialize Vertex AI
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    aiplatform.init(project=project_id, location=location)

    # Prepare the prompt for summarization
    log_messages = [entry.get("@message", "") for entry in log_entries if entry.get("@message")]
    combined_logs = "\n".join(log_messages)

    if not combined_logs:
        return "No log entries to summarize."

    prompt = f"Summarize the following log entries for an incident review. Focus on key errors, warnings, and any unusual patterns:\n\n{combined_logs}\n\nIncident Summary:"

    # Use the Gemini Pro model for summarization
    model = aiplatform.preview.language_models.ChatModel.from_pretrained("gemini-pro")

    print("Sending log entries to Vertex AI for summarization...")
    response = model.predict(prompt)
    print("Summarization complete.")

    return response.text
