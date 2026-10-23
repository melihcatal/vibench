from google.cloud import aiplatform

def summarize_incident_logs(project_id: str, location: str, log_entries: list) -> str:
    """
    Summarizes error-log findings for incident review using Google Cloud Generative AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region for Vertex AI (e.g., "us-central1").
        log_entries (list): A list of log entry dictionaries to summarize.

    Returns:
        str: A summary of the incident based on the log entries.
    """

    aiplatform.init(project=project_id, location=location)

    # Using the pre-trained text-bison model for summarization
    # You might need to adjust the model name based on availability and desired quality
    model = aiplatform.get_model_by_name(f"projects/{project_id}/locations/{location}/models/text-bison@001")

    # Concatenate relevant parts of log entries into a single text for summarization
    # In a real scenario, you'd likely extract specific fields from log_entries
    # and format them more carefully for the LLM.
    combined_logs_text = "\n".join([
        f"Severity: {entry.get('severity', 'UNKNOWN')}, Message: {entry.get('textPayload') or entry.get('jsonPayload')}"
        for entry in log_entries
    ])

    if not combined_logs_text:
        return "No log entries provided for summarization."

    prompt = f"Please summarize the following error logs for an incident review. Highlight key issues, potential root causes, and affected areas:\n\n{combined_logs_text}"

    response = model.predict(prompt=prompt)

    return response.text
