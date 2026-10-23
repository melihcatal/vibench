from observability_client import get_logging_client
from observability_models import LogEntry
from typing import List

def write_correlated_log_events(log_entries: List[LogEntry], correlation_id: str):
    client = get_logging_client()
    
    if not log_entries:
        return

    entries_to_write = []
    for entry in log_entries:
        payload_with_correlation = entry.payload.copy()
        payload_with_correlation["correlationId"] = correlation_id
        
        entry_data = {
            "jsonPayload": payload_with_correlation,
            "severity": entry.severity,
            "logName": f"projects/{client.project}/logs/{entry.log_name}",
            "resource": {
                "type": entry.resource_type,
                "labels": entry.resource_labels
            }
        }
        entries_to_write.append(entry_data)
    
    client.write_entries(entries_to_write)