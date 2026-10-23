import os
import json
import requests
from observability_client import get_azure_tenant_id, get_azure_client_id


def write_correlated_logs(events: list[dict], correlation_id: str):
    """Write correlated application log events to Azure Monitor Logs Ingestion API.
    Each `events` item must be a dict representing a log record.
    The `correlation_id` is added to tags for traceability.
    """
    tenant = get_azure_tenant_id()
    client = get_azure_client_id()
    endpoint = (
        f"https://{tenant}.ods.opinsights.azure.com/api/logs?api-version=2020-08-01"
    )
    payload = {
        "type": "CustomLogs",
        "records": [{**ev, "correlation_id": correlation_id} for ev in events],
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {client}",
        "Log-Type": "CustomLogs",
    }
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
