import json, logging, os, time, boto3
from observability_models import LogEvent

def incident_summary(log_events):
    """Summarize a list of LogEvent dicts for incident review.

    Produces a concise human-readable report.
    """
    if not log_events:
        return "No logs provided."
    # Convert each log to a dict with only needed fields
    events = [json.loads(ev['message']) for ev in log_events]
    # Group by severity
    severity_counts = {}
    for ev in events:
        severity_counts[ev.get('severity', 'UNKNOWN')] = severity_counts.get(ev.get('severity', 'UNKNOWN'), 0) + 1

    # Extract recent timestamps
    recent = sorted([ev['timestamp'] for ev in events], reverse=True)[:5]
    recent_times = [datetime.datetime.fromtimestamp(ts/1000).isoformat() for ts in recent]

    summary = [
        f"Incident Summary ({len(events)} events):",
        f"- Total errors: {severity_counts.get('ERROR', 0)}",
        f"- Total warnings: {severity_counts.get('WARN', 0) + severity_counts.get('WARNING', 0)}",
        f"- Most recent timestamps: {', '.join(recent_times)}",
    ]
    return "\n".join(summary)

# CLI wrapper for quick manual use
def main():
    # Example usage: read recent error logs via fetch utility (not implemented here)
    # For demo, assume we can call fetch helper
    from fetch_recent_logs import fetch_recent_logs
    recent = fetch_recent_logs(field='level', value='ERROR')
    print(incident_summary(recent))

if __name__ == '__main__':
    main()
