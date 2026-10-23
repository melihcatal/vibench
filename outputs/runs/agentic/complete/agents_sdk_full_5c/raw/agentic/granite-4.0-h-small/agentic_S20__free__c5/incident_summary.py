import json
from collections import Counter
from typing import List, Dict
from observability_models import LogPayload
from observability_client import get_log_client

def summarize_error_logs(error_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Creates a concise incident summary from a list of error logs.

    Returns a dictionary containing:
      - total_errors
      - top_error_messages (count of each distinct message)
      - top_services (services with most errors)
    """
    total = len(error_logs)
    # Count messages
    messages = Counter()
    services = Counter()
    for entry in error_logs:
        msg = entry.get("message", "<no-message>")
        srv = entry.get("service", "<unknown>")
        messages[msg] += 1
        services[srv] += 1
    summary = {
        "total_errors": total,
        "top_error_messages": dict(messages.most_common(5)),
        "top_services": dict(services.most_common(5)),
    }
    return summary

if __name__ == "__main__":
    # Example: fetch recent ERROR logs and summarize
    from query_error_logs import query_error_logs
    errors = query_error_logs(severity="ERROR", start_hours=12)
    summary = summarize_error_logs(errors)
    print(json.dumps(summary, indent=2))