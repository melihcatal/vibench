from observability_client import get_openai_client
from observability_models import LogEntry
from typing import List

def summarize_incident_logs(log_entries: List[LogEntry]) -> str:
    openai_client = get_openai_client()

    if not log_entries:
        return "No log entries provided for summarization."

    log_texts = []
    for entry in log_entries:
        timestamp_str = entry.timestamp.isoformat() if entry.timestamp else "N/A"
        severity_str = entry.severity if entry.severity else "N/A"
        payload_str = entry.text_payload if entry.text_payload else str(entry.json_payload)
        log_texts.append(f"[{timestamp_str}] [{severity_str}] {payload_str}")

    combined_logs = "\n".join(log_texts)

    prompt = (
        "Analyze the following log entries and provide a concise summary of the incident, "
        "identifying potential root causes, affected components, and key events. "
        "Keep the summary to a maximum of 3-5 sentences.\n\n"
        f"Log Entries:\n```\n{combined_logs}\n```"
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an incident analyst tasked with summarizing logs."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content
