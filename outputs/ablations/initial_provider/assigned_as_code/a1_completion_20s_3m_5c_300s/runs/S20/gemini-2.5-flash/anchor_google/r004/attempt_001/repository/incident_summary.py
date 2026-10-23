from observability_client import ObservabilityClient
from observability_models import IncidentSummaryRequest, LogEntry

def incident_summary(project_id: str, log_entries: list[dict], summary_length: str = "short"):
    client = ObservabilityClient(project_id=project_id)
    
    # Convert dicts back to LogEntry models for type safety/consistency if needed, or directly use dicts
    # For simplicity, we'll work with the dicts for generating the prompt
    
    log_texts = [f"[{entry.get('timestamp', '')}] {entry.get('severity', '')}: {entry.get('message', '')}" for entry in log_entries]
    combined_logs = "\n".join(log_texts)

    prompt = f"""Summarize the following error logs for an incident review. Focus on identifying the root cause, impacted areas, and potential solutions. The summary should be {summary_length}.\n\nLogs:\n{combined_logs}"""

    summary = client.generate_content(prompt)
    
    return {"summary": summary}
