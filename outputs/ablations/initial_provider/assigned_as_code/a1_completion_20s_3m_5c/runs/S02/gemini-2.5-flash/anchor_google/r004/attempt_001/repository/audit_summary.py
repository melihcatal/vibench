import os
from datadog import initialize, api
from typing import List, Dict, Any


def summarize_audit_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")

    if not api_key or not app_key:
        return {"status": "error", "message": "DATADOG_API_KEY and DATADOG_APP_KEY must be set as environment variables."}

    initialize(api_key=api_key, app_key=app_key)

    summary_message = f"Received {len(events)} federated login audit events.\n"
    user_logins = {}
    for event in events:
        user_id = event.get("user_id", "unknown_user")
        event_type = event.get("event_type", "unknown_event")
        timestamp = event.get("timestamp", "unknown_time")

        if user_id not in user_logins:
            user_logins[user_id] = {"total_logins": 0, "last_login": None}
        user_logins[user_id]["total_logins"] += 1
        if not user_logins[user_id]["last_login"] or timestamp > user_logins[user_id]["last_login"]:
            user_logins[user_id]["last_login"] = timestamp

        # Send each event as a log to Datadog
        api.Metric.send('federated.login.event', 1, tags=[f'user_id:{user_id}', f'event_type:{event_type}'])
        api.Event.create(title="Federated Login Event", text=f"User: {user_id}, Type: {event_type}, Details: {event.get("details")}", tags=[f'user_id:{user_id}', f'event_type:{event_type}'])

    summary_message += "User Login Summary:\n"
    for user_id, data in user_logins.items():
        summary_message += f" - User {user_id}: {data["total_logins"]} logins, last at {data["last_login"]}\n"

    # Send a summary event to Datadog
    api.Event.create(title="Federated Login Audit Summary", text=summary_message, tags=["federated_login", "audit_summary"])

    return {"status": "success", "summary": summary_message}
