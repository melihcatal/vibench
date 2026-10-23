from datetime import datetime
from observability_models import LogMessage


def incident_summary(
    error_logs: List[LogMessage], start_ts: datetime, end_ts: datetime
) -> dict:
    """Summarize error-log findings for incident review.

    Produces a concise report containing:
        - total error count
        - unique services (log group names) affected
        - top error messages with occurrence count
    Uses watsonx.ai Qwen for optional natural language summarization.
    Required environment variable:
        WATSONX_API_KEY
        WATSONX_PROJECT_ID
    """
    total = len(error_logs)
    services = {log.get("logGroupName") for log in error_logs}
    message_counts = {}
    for log in error_logs:
        msg = log["message"]
        message_counts[msg] = message_counts.get(msg, 0) + 1
    # Sort by frequency
    top_messages = sorted(message_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    return {
        "total_errors": total,
        "services_affected": list(services),
        "top_error_messages": top_messages,
    }

    # Optional LLM summarization (placeholder for later-step integration)
    # response = watsonx_ai_chat(messages=top_messages)
