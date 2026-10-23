from datetime import datetime, timezone
import time
from typing import Dict, Any
from observability_client import ObservabilityClient
from observability_models import LogEvent

def write_correlated_logs(log_events: list[LogEvent], config: Dict[str, Any]):
    client_wrapper = ObservabilityClient(ingestion_endpoint=config['ingestion_endpoint'])
    ingestion_client = client_wrapper.get_ingestion_client()

    logs_to_upload = []
    for log_event in log_events:
        timestamp_ms = config.get('timestamp_ms', time.time() * 1000)
        event = {
            'TimeGenerated': datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat(),
            'EventName': log_event.event_name,
            'Severity': log_event.severity,
            'Message': log_event.message,
            **log_event.properties
        }
        if log_event.correlation_id:
            event['CorrelationId'] = log_event.correlation_id
        logs_to_upload.append(event)

    ingestion_client.upload(rule_id=config['rule_id'], stream_name=config['stream_name'], logs=logs_to_upload)
    return {'submitted_count': len(logs_to_upload)}
