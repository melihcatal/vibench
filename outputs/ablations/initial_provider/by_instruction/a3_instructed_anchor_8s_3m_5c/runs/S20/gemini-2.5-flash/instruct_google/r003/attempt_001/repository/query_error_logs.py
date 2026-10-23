from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import LogQuery, LogEntry

def query_error_logs(time_range_minutes: int = 60, min_severity: str = "ERROR") -> list[LogEntry]:
    client = ObservabilityClient()

    now = datetime.utcnow()
    time_filter = now - timedelta(minutes=time_range_minutes)
    
    # Google Cloud Logging filter syntax
    filter_string = (
        f'severity>="{min_severity}" AND '
        f'timestamp>="{time_filter.isoformat('T')}"
    )

    # Using list_entries with filter
    # The list_entries method returns an iterator, we convert to a list for this example
    # Note: page_size can be adjusted based on expected results volume
    entries_iterator = client.list_entries(filter_=filter_string, order_by="timestamp desc", page_size=100)
    
    error_logs: list[LogEntry] = []
    for entry in entries_iterator:
        # Google Cloud Logging entry object has attributes like timestamp, severity, payload
        # We need to normalize it to our LogEntry model
        json_payload = None
        if entry.payload_type == 'json':
            json_payload = entry.json_payload
        elif entry.payload_type == 'text':
            json_payload = {"message": entry.text_payload}
        elif entry.payload_type == 'proto':
            json_payload = {"message": str(entry.proto_payload)}

        error_logs.append(LogEntry(
            timestamp=entry.timestamp.isoformat(),
            severity=entry.severity,
            message=json_payload.get("message", ""), # Extract message from json_payload if available
            resource_type=entry.resource.type if entry.resource else "unknown",
            resource_labels=entry.resource.labels if entry.resource else {},
            json_payload=json_payload
        ))
    return error_logs

if __name__ == "__main__":
    # Example Usage: Query errors from the last 30 minutes with severity ERROR or higher
    recent_errors = query_error_logs(time_range_minutes=30, min_severity="ERROR")
    for log in recent_errors:
        print(f"[{log.timestamp}] {log.severity}: {log.message} (Resource: {log.resource_type})")
