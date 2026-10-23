from datadog import api
from identity_client import initialize_datadog
import time


def get_recent_login_summary(hours_ago=24):
    """
    Summarizes federated-login audit events from Datadog.
    """
    initialize_datadog()

    end = int(time.time())
    start = end - (hours_ago * 3600)

    # Example query for events tagged with 'federated_login'
    query_result = api.Event.query(
        start=start, end=end, tags="application:federated_login"
    )

    summary = {"total_events": 0, "event_counts_by_title": {}}

    if "events" in query_result:
        events = query_result["events"]
        summary["total_events"] = len(events)
        for event in events:
            title = event.get("title", "Untitled Event")
            summary["event_counts_by_title"][title] = (
                summary["event_counts_by_title"].get(title, 0) + 1
            )

    return summary
