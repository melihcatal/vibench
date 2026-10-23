import os
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_sort import LogsSort
from datetime import datetime, timedelta

def summarize_audit_events(user_id: str, time_range_minutes: int = 60):
    # Initialize Datadog client
    # Ensure DATADOG_API_KEY and DATADOG_APP_KEY are set in environment variables
    # Datadog host can be configured via DATADOG_HOST or default to https://api.datadoghq.com

    api_key = os.environ.get("DATADOG_API_KEY", "YOUR_DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY", "YOUR_DATADOG_APP_KEY")

    if not api_key or not app_key:
        raise ValueError("DATADOG_API_KEY and DATADOG_APP_KEY must be set in environment variables.")

    # Configure Datadog API client
    from datadog_api_client.v2.configuration import Configuration
    configuration = Configuration(
        api_key={
            'apiKeyAuth': api_key,
            'appKeyAuth': app_key
        }
    )

    logs_api = LogsApi(configuration)

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=time_range_minutes)

    query = f"source:federated-login @user.id:{user_id}"

    request = LogsListRequest(
        filter={
            "query": query,
            "_from": start_time.isoformat() + "Z",
            "to": now.isoformat() + "Z",
        },
        sort=LogsSort.TIMESTAMP_ASCENDING,
        page=LogsListRequestPage(limit=100) # Limit to 100 logs for summary
    )

    try:
        response = logs_api.list_logs(body=request)
        summary = []
        event_counts = {}
        for log in response.data:
            message = log.attributes.message
            status = log.attributes.status
            timestamp = log.attributes.timestamp
            summary.append(f"[{timestamp}] [{status.value}] {message}")
            event_counts[status.value] = event_counts.get(status.value, 0) + 1

        return {
            "user_id": user_id,
            "total_events": len(summary),
            "event_counts": event_counts,
            "events": summary
        }
    except Exception as e:
        return {"error": f"Failed to retrieve logs from Datadog: {e}"}
