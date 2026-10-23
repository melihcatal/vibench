import json
import pandas as pd
from query_error_logs import query_error_logs
from observability_models import LogNormalization, NormalizedLog

def summarize_error_incidents(error_logs):
    """Summarize recent error logs for incident review.

    - Count incidents per service
    - Identify top error messages
    - Compute time window of the incident
    - Produce a concise text summary
    """
    # Normalize logs to a DataFrame
    norm_logs = [LogNormalization.from_dict(l) for l in error_logs]
    df = pd.DataFrame([l.to_dict() for l in norm_logs])
    summary = {}

    # 1. Incident count per service
    summary["incidents_by_service"] = df["service"].value_counts().to_dict()

    # 2. Most frequent error messages
    top_messages = (
        df.groupby(["service", "message"])\n          .size()\n          .sort_values(ascending=False)\n          .head(5)\n          .reset_index(name=\"count\")\n          .to_dict(orient=\"records\")
    )
    summary["top_error_messages"] = top_messages

    # 3. Incident time window
    timestamps = df["timestamp"].astype("datetime64[ns]")
    summary["time_window"] = {
        "start": timestamps.min().isoformat(),
        "end": timestamps.max().isoformat()
    }

    # 4. Concise text summary
    lines = [
        f"Incident Summary ({timestamps.min()} – {timestamps.max()})",
        f"Total error events: {len(df)}",
        "Events per service:",
    ]
    for svc, cnt in summary["incidents_by_service"].items():
        lines.append(f"  - {svc}: {cnt} errors")
    lines.append("Top error messages:")
    for msg in summary["top_error_messages"]:
        lines.append(f"  - {msg['service']}: \"{msg['message']}\" – {msg['count']} occurrences")
    return "\\n".join(lines)

if __name__ == "__main__":
    logs = query_error_logs()
    print(summarize_error_incidents(logs))
