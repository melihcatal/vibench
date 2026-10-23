import os
from typing import List, Dict, Any
from google.cloud import aiplatform
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def incident_summary(error_logs: List[Dict[str, Any]]) -> str:
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = os.environ.get('GOOGLE_CLOUD_LOCATION', 'global')
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    # For simplicity, we'll concatenate the log messages into a single prompt.
    # In a real-world scenario, you might want to preprocess or chunk these logs.
    log_messages = [log.get('message', '') for log in error_logs]
    combined_log_text = "\n".join(log_messages)

    if not combined_log_text:
        return "No error logs provided for summarization."

    # Construct the summary prompt
    summary_prompt = (
        "Please summarize the following error logs, identifying key issues, "
        "potential root causes, and any recurring patterns. "
        "Provide a concise summary suitable for an incident review meeting.\n\n"
        f"Error Logs:\n{combined_log_text}"
    )

    try:
        response = model.generate_content(summary_prompt)
        return response.text

    except Exception as e:
        return f"Error during incident summarization with Google Cloud Generative AI: {e}"

