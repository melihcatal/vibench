from observability_client import clients
from observability_models import LogQueryResult
from typing import List

def summarize_incident_logs(error_logs: List[LogQueryResult]) -> str:
    """
    Summarizes error log findings for incident review using OpenAI.
    """
    if not error_logs:
        return "No error logs provided for summarization."

    openai_client = clients.openai_client

    log_messages = [f"Timestamp: {log.timestamp}, Severity: {log.severity}, Message: {log.message}" for log in error_logs]
    
    prompt = (
        "You are an incident response assistant. Summarize the following error logs into a concise incident report. "
        "Highlight key issues, potential root causes, and recurring patterns if any. "
        "Include timestamps where relevant.\n\n"
        "Error Logs:\n" + "\n".join(log_messages[:10])
    )
    if len(log_messages) > 10:
        prompt += f"\n... (and {len(log_messages) - 10} more logs)"

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes technical incident logs."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    
    summary = response.choices[0].message.content
    return summary
