from google.cloud import logging_v2
from vertexai.preview.generative_models import GenerativeModel, Part
import datetime

def summarize_error_logs(project_id: str, time_range_seconds: int = 3600) -> str:
    """
    Summarizes recent error log entries for incident review using Google Cloud Logging and Vertex AI.

    Args:
        project_id: The Google Cloud project ID.
        time_range_seconds: The duration in seconds to fetch logs from the past. Defaults to 1 hour.

    Returns:
        A string containing the summary of error logs.
    """
    logging_client = logging_v2.Client(project=project_id)
    
    now = datetime.datetime.utcnow()
    past = now - datetime.timedelta(seconds=time_range_seconds)
    
    filter_string = (
        f'severity >= ERROR AND '
        f'timestamp >= "{past.isoformat("T")}Z" AND '
        f'timestamp < "{now.isoformat("T")}Z"'
    )
    
    log_messages = []
    for entry in logging_client.list_entries(filter_=filter_string, projects=[f"projects/{project_id}"]):
        if entry.text_payload:
            log_messages.append(entry.text_payload)
        elif entry.json_payload:
            log_messages.append(str(entry.json_payload))
        elif entry.proto_payload:
            log_messages.append(str(entry.proto_payload))

    if not log_messages:
        return "No error logs found in the specified time range."

    # Use Vertex AI for summarization
    model = GenerativeModel("gemini-pro")
    
    prompt = (
        "Summarize the following error logs for an incident review. "
        "Highlight key issues, potential root causes, and frequency of errors:

"
    )
    prompt += "\n".join(log_messages[:100]) # Limit to 100 log messages to avoid exceeding token limits

    response = model.generate_content(prompt)
    
    return response.text
