from datetime import datetime
from observability_client import get_logs_query_client
from azure.monitor.query import LogsBatchQuery
from observability_models import LogEntry

def write_correlated_logs(log_entries):
    client = get_logs_query_client()
    body = [{
        'Time': entry.timestamp.isoformat(),
        'Level': entry.level,
        'Message': entry.message,
        'CorrelationId': entry.correlation_id,
    } for entry in log_entries]
    query = LogsBatchQuery(body)
    client.query_batch('MyWorkspace', query)

log_entries = [
    LogEntry(datetime.utcnow(), 'Info', 'First log entry', '12345'),
    LogEntry(datetime.utcnow(), 'Info', 'Second log entry', '12345'),
]
write_correlated_logs(log_entries)