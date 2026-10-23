import json
from typing import List, Dict
from observability_client import get_log_client, normalize_query_response


def summarize_incident(
    events: List[Dict[str, Any]], summary_title: str = "Incident Summary"
) -> Dict[str, Any]:
    """Produce a concise incident review document from aggregated log events.

    The function demonstrates how to:
    1. Gather error logs (could be from query_error_logs or fetch_recent_logs)
    2. Group by error message or request ID
    3. Count occurrences
    4. Include top‑N examples for each group
    5. Return a JSON‑compatible structure that can be stored or presented.
    """
    client = get_log_client()
    # Example: assume events is already a list of filtered logs (e.g., from query_error_logs)
    # For demonstration we will just use the passed events list
    groups: Dict[str, List[Dict]] = {}
    for ev in events:
        # Use a composite key: severity + message (or correlation_id if present)
        key = ev.get("message", "<no_message>")
        groups.setdefault(key, []).append(ev)
    summary = {
        "title": summary_title,
        "generated_at": "2024-01-01T00:00:00Z",
        "group_counts": {k: len(v) for k, v in groups.items()},
        "top_examples": {
            k: v[:3]  # show first three logs for each group
            for k, v in groups.items()
        },
    }
    # Persist the summary to the same logging service or a separate incident store
    client.log_structured(summary, level="info")
    return summary
