import os
from datetime import datetime, timedelta
from datadog import initialize, api


def summarize_login_audit_events(start_time: datetime, end_time: datetime):
    options = {
        "api_key": os.environ.get("DATADOG_API_KEY"),
        "app_key": os.environ.get("DATADOG_APP_KEY"),
    }
    initialize(**options)

    query = 'source:oauth "login" "success"'

    events = api.Event.query(
        start=int(start_time.timestamp()), end=int(end_time.timestamp()), query=query
    )

    summary = {
        "total_events": len(events.get("events", [])),
        "time_range": {"start": start_time.isoformat(), "end": end_time.isoformat()},
        "provider_breakdown": {},
        "success_rate": 0,
        "events": [],
    }

    success_count = 0
    for event in events.get("events", []):
        provider = event.get("tags", {}).get("provider", "unknown")
        summary["provider_breakdown"][provider] = (
            summary["provider_breakdown"].get(provider, 0) + 1
        )

        if "success" in event.get("text", "").lower():
            success_count += 1

        summary["events"].append(
            {
                "id": event.get("id"),
                "title": event.get("title"),
                "text": event.get("text"),
                "timestamp": event.get("date_happened"),
                "provider": provider,
            }
        )

    if summary["total_events"] > 0:
        summary["success_rate"] = (success_count / summary["total_events"]) * 100

    return summary
