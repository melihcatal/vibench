from datetime import datetime
from observability_client import get_logs_query_client
from azure.monitor.query import LogsBatchQuery

def write_structured_log(log_entry):
    client = get_logs_query_client()
    body = [{
        'Time': log_entry.timestamp.isoformat(),
        'Level': log_entry.level,
        'Message': log_entry.message,
    }]
    query = LogsBatchQuery(body)
    client.query_batch('MyWorkspace', query)

log_entry = LogEntry(datetime.utcnow(), 'Info', 'This is a test log entry')
write_structured_log(log_entry)