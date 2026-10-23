import json
from observability_models import LogResult

def incident_summary(logs: LogResult) -> str:
    """Summarize error‑log findings for incident review.

    Generates a concise markdown summary that includes:
    - Total number of error logs
    - Top error types or messages
    - Occurrence timestamps window
    - Recommended next steps
    """
    total = logs.total
    if not logs.logs:
        return f"No error logs found (total: {total})."

    # Simple aggregation: count occurrences of each message
    from collections import Counter
    message_counter = Counter(log["message"] for log in logs.logs)
    top_messages = message_counter.most_common(5)

    # Determine time window of the retrieved logs
    timestamps = [json.loads(json.dumps(log)) for log in logs.logs]  # naive conversion to dict
    # Assume logs are already sorted; grab first and last timestamps
    timestamps = sorted(timestamps, key=lambda x: x["timestamp"])
    window = f"{timestamps[0][\"timestamp\"]} – {timestamps[-1][\"timestamp\"]}"

    summary = (
        f"## Incident Summary\n\n- **Total error logs:** `{total}`\n"
        f"- **Time window:** `{window}`\n"
        f"- **Top error messages:**\n"
    )
    for msg, count in top_messages:
        summary += f"  - `{msg}` × {count}\n"

    summary += (
        "\n**Recommendations:**\n- Investigate the top error messages for root cause.\n- Correlate with recent deployments or configuration changes.\n- Review affected services/components for impacted users."
    )
    return summary
