import os
import json
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part

from observability_client import get_generative_model
from observability_models import IncidentSummary, QueryResult

# Initialize Vertex AI client, typically done once at application startup
# aiplatform.init(project=os.environ.get("GCP_PROJECT_ID"), location=os.environ.get("GCP_REGION", "us-central1"))

def summarize_error_logs(error_logs: list[QueryResult]) -> IncidentSummary:
    if not error_logs:
        return IncidentSummary(
            title="No Errors Found",
            impact_assessment="No error logs were provided for summarization.",
            relevant_log_ids=[]
        )

    model = get_generative_model(model_name="gemini-pro") # Using Gemini-Pro model

    log_texts = []
    relevant_log_ids = []
    for log in error_logs:
        log_texts.append(f"Timestamp: {log.timestamp}, Severity: {log.severity}, Message: {log.message}")
        if log.log_id not in relevant_log_ids:
            relevant_log_ids.append(log.log_id)

    prompt_parts = [
        "Review the following error log entries and provide a concise incident summary.",
        "Identify the main issue, assess potential impact, hint at possible root causes, and suggest immediate actions.",
        "Format the output as a JSON object with 'title', 'impact_assessment', 'root_cause_hint', and 'suggested_actions' (list of strings).",
        "Log Entries:\n" + "\n".join(log_texts)
    ]

    response = model.generate_content(
        prompt_parts,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 500
        }
    )

    try:
        summary_data = json.loads(response.text)
        return IncidentSummary(
            title=summary_data.get("title", "Incident Summary"),
            impact_assessment=summary_data.get("impact_assessment", "Could not assess impact."),
            root_cause_hint=summary_data.get("root_cause_hint"),
            suggested_actions=summary_data.get("suggested_actions"),
            relevant_log_ids=relevant_log_ids
        )
    except json.JSONDecodeError:
        # Fallback if the model doesn't return perfect JSON
        return IncidentSummary(
            title="Incident Summary Error",
            impact_assessment="Could not parse summary from AI. Raw response: " + response.text,
            relevant_log_ids=relevant_log_ids
        )

