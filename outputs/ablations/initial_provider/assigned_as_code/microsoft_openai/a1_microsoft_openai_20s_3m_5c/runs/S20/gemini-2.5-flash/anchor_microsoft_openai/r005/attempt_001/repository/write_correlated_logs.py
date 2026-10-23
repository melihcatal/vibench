import os
import time
from datetime import datetime, timezone
from observability_client import get_logs_ingestion_client
from observability_models import CorrelatedLogEvent


def write_correlated_logs(event: CorrelatedLogEvent, config=None):
    config = config or {}
    ingestion_endpoint = os.environ.get("AZURE_LOGS_INGESTION_ENDPOINT", config.get("endpoint"))
    rule_id = os.environ.get("AZURE_LOGS_INGESTION_RULE_ID", config.get("rule_id"))
    stream_name = os.environ.get("AZURE_LOGS_INGESTION_STREAM_NAME", config.get("stream_name"))

    if not all([ingestion_endpoint, rule_id, stream_name]):
        raise ValueError("Missing Azure Logs Ingestion configuration: endpoint, rule_id, or stream_name.")

    client = get_logs_ingestion_client(ingestion_endpoint)

    log_entry = {
        "TimeGenerated": event.timestamp.isoformat(),
        "Message": event.message,
        "Severity": event.severity,
        "CorrelationId": event.correlation_id,
        **event.properties
    }

    with client:
        client.upload(rule_id=rule_id, stream_name=stream_name, logs=[log_entry])
    return {'submitted': True}
