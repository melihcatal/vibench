import os
from datetime import datetime, timezone
from observability_client import ObservabilityClient
from observability_models import CorrelatedLogEntry

def write_correlated_logs(service_name: str, session_id: str, messages: list[str]):
    client = ObservabilityClient()
    current_time = datetime.now(timezone.utc).isoformat()

    for i, message in enumerate(messages):
        log_entry = CorrelatedLogEntry(
            message=message,
            severity="Informational",
            timestamp=current_time,
            correlation_id=session_id,
            resource_id=f"/subscriptions/{os.environ.get('AZURE_SUBSCRIPTION_ID')}/resourceGroups/{os.environ.get('AZURE_RESOURCE_GROUP')}/providers/Microsoft.OperationalInsights/workspaces/{client.workspace_id}",
            properties={
                "ServiceName": service_name,
                "SequenceNum": i + 1
            }
        )
        client.ingest_log(log_entry)
    return {"status": "correlated logs submitted", "correlation_id": session_id}
