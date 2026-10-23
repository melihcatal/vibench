import os
from datetime import datetime, timedelta
from observability_client import get_log_client


def fetch_recent_logs(
    field: str = "severity", value: str = "ERROR", minutes: int = 30
) -> list[dict]:
    """Fetches recent logs filtered by a field/value pair and a time window.

    Uses the Azure Monitor Logs (REST) endpoint via the azure-monitor-query SDK.
    """
    client = (
        get_log_client()
    )  # Azure Monitor client with AZURE_TENANT_ID, AZURE_CLIENT_ID, etc.
    end = datetime.utcnow()
    start = end - timedelta(minutes=minutes)
    query = f"{field} == '{value}'"
    results = client.query(
        workspace_id=os.getenv("AZURE_LOG_ANALYTICS_WORKSPACE_ID"),
        query=query,
        time_range={"from": start.isoformat() + "Z", "to": end.isoformat() + "Z"},
    )
    return results.records
