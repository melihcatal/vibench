from observability_client import get_generative_model
from observability_models import LogEntry

def incident_summary(error_logs: list[LogEntry]) -> str:
    model = get_generative_model("gemini-pro") # Using gemini-pro for summarization

    if not error_logs:
        return "No error logs provided for summarization."

    log_texts = []
    for log in error_logs:
        log_texts.append(f"Severity: {log.severity}, Timestamp: {log.timestamp.isoformat()}, Message: {log.message}")

    prompt = (
        "Summarize the following error logs for an incident review. "
        "Focus on key issues, potential root causes, and frequency of errors.\n\n"
        + "\n".join(log_texts)
    )

    response = model.generate_content(prompt)
    return response.text
