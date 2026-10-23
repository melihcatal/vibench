from datetime import datetime, timezone
import time
import os
from typing import Dict, Any, List
from observability_client import ObservabilityClient
from observability_models import CorrelatedLogEvent

def write_correlated_logs(log_events: List[Dict[str, Any]], config: Dict[str, Any] = None):
    config = config or {}
    observability_client = ObservabilityClient(config)
    ingestion_client = observability_client.get_logs_ingestion_client()

    # The rule_id and stream_name should be configured for the ingestion client
    # These can come from the config dict or environment variables
    rule_id = config.get('LOG_INGESTION_RULE_ID', os.environ.get('AZURE_LOG_INGESTION_RULE_ID'))
    stream_name = config.get('LOG_INGESTION_STREAM_NAME', os.environ.get('AZURE_LOG_INGESTION_STREAM_NAME'))

    if not rule_id or not stream_name:
        raise ValueError("Log Ingestion Rule ID or Stream Name not configured.")

    logs_to_upload = []
    for event_data in log_events:
        timestamp_ms = event_data.get('timestamp_ms', time.time() * 1000)
        log_event = CorrelatedLogEvent(
            TimeGenerated=datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat(),
            message=event_data['message'],
            correlation_id=event_data['correlation_id'],
            severity=event_data.get('severity', 'Informational'),
            properties=event_data.get('properties', {})
        )
        logs_to_upload.append(log_event.__dict__)

    ingestion_client.upload(rule_id=rule_id, stream_name=stream_name, logs=logs_to_upload)

    return {'submitted_count': len(logs_to_upload)}
