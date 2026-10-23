from typing import List, Dict
from anthropic import Anthropic
from observability_client import get_logging_client
from observability_models import LogQueryResponse


def summarize_error_logs(log_entries: List[Dict[str, Any]]) -> str:
    """
    Summarizes error log findings for incident review using Anthropic's Claude model.

    Args:
        log_entries: List of log entries to summarize.

    Returns:
        A summary of the error logs for incident review.
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Prepare log data for summarization
    log_text = "\n".join(
        [
            f"Timestamp: {entry.get('timestamp')}, Severity: {entry.get('severity')}, Message: {entry.get('jsonPayload', {}).get('message', 'No message')}"
            for entry in log_entries
        ]
    )

    # Create prompt for summarization
    prompt = f"Please summarize the following error logs for an incident review. "
    prompt += f"Focus on identifying root causes, impacted services, and potential resolutions:\n\n{log_text}"

    # Call Anthropic API
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text
