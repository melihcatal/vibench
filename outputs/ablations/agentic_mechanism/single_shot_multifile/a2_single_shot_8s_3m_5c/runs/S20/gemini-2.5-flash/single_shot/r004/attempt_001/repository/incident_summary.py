import os
from typing import List
from observability_client import get_generative_model
from observability_models import LogEntry, IncidentSummary

def summarize_incident_logs(error_logs: List[LogEntry]) -> IncidentSummary:
    if not error_logs:
        return IncidentSummary(
            title="No Errors Found",
            description="No error logs were provided for summarization.",
            severity="INFO",
            recommended_action="Monitor systems.",
            related_logs=[]
        )

    model = get_generative_model(model_name="gemini-pro")

    log_texts = []
    for log in error_logs:
        payload_str = str(log.json_payload) if log.json_payload else ''
        log_texts.append(f"Timestamp: {log.timestamp}, Severity: {log.severity}, Message: {log.message}, Payload: {payload_str}")

    prompt = (
        "Analyze the following error log entries and provide a concise incident summary. "
        "Include a title, a description of the problem, an overall severity (e.g., CRITICAL, HIGH, MEDIUM, LOW), "
        "and a recommended action. Format the output as a JSON object with keys: title, description, severity, recommended_action.\n\n"
        "Log Entries:\n" + "\n".join(log_texts)
    )

    response = model.generate_content(prompt)
    summary_text = response.text

    # Attempt to parse as JSON. If it fails, return a default structured summary.
    try:
        import json
        parsed_summary = json.loads(summary_text)
        return IncidentSummary(
            title=parsed_summary.get('title', 'Generated Incident Summary'),
            description=parsed_summary.get('description', 'Could not parse description.'),
            severity=parsed_summary.get('severity', 'UNKNOWN'),
            recommended_action=parsed_summary.get('recommended_action', 'Review logs manually.'),
            related_logs=error_logs
        )
    except json.JSONDecodeError:
        return IncidentSummary(
            title="Automated Summary Failed",
            description=f"Failed to parse LLM output as JSON. Raw output: {summary_text}",
            severity="WARNING",
            recommended_action="Manually review logs and LLM output.",
            related_logs=error_logs
        )

