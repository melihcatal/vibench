import datetime
from observability_client import LogClient, QueryParams


def query_error_logs(
    severity: str = "ERROR",
    start_time: datetime.datetime = None,
    end_time: datetime.datetime = None,
) -> list[dict]:
    """Query recent error log entries filtered by severity and time range.

    Uses Azure Monitor Logs (Logs Ingestion API) as the concrete query service.
    Required environment variables:
        AZURE_TENANT_ID
        AZURE_CLIENT_ID
        AZURE_CLIENT_SECRET
        AZURE_SUBSCRIPTION_ID
        RESOURCE_GROUP
        WORKSPACE_NAME
    """
    client = LogClient()  # Azure Monitor client initialized in helper
    params = QueryParams(
        schema="AzureDiagnostics", filter=f"SeverityLevel == '{severity}'"
    )
    if start_time:
        params.start = start_time.isoformat()
    if end_time:
        params.end = end_time.isoformat()
    results = client.query(params)
    return results
