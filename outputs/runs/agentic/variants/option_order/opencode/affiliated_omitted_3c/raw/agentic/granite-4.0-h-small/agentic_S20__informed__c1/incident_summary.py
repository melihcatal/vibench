import json
import os
from datetime import datetime, timedelta
from observability_client import get_query_client
from observability_models import QueryResult


def incident_summary(start_minutes: int = 60, severity: str = "ERROR") -> str:
    """Summarizes recent error logs for incident review.

    Queries logs for the past `start_minutes` minutes filtered by `severity`.
    Returns a concise markdown summary containing count, services, and example messages.
    """
    client = get_query_client()
    end_iso = datetime.utcnow().isoformat() + "Z"
    start_iso = (datetime.utcnow() - timedelta(minutes=start_minutes)).isoformat() + "Z"
    query = {
        "filter": {
            "severity": severity,
            "timestamp_range": {
                "start": start_iso,
                "end": end_iso,
            },
        },
    }
    result: QueryResult = client.query(query)
    total = result.get("total", 0)
    services = {evt["service"] for evt in result.get("events", [])}
    sample_msgs = [evt["message"] for evt in result.get("events", [])[:5]]
    summary = (
        f"# Incident Summary ({severity} logs in last {start_minutes} minutes)\n"
        f"- **Total matching events:** {total}\n"
        f"- **Affected services:** {', '.join(services) if services else 'N/A'}\n"
        f"- **Sample messages:**\n"
        f"  - {sample_msgs[0] if sample_msgs else 'No sample messages.'}\n"
    )
    return summary
