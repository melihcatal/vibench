from observability_client import CLOUDWATCH_LOGS
from observability_models import LogEntry

def write_correlated_logs(log_group, log_stream, correlation_id, log_entries):
    for log_entry in log_entries:
        log_entry.message = f'[{correlation_id}] {log_entry.message}'
        write_log(log_group, log_stream, log_entry)

log_entries = [
    LogEntry('Correlated log event 1', '2023-10-01T12:00:00'),
    LogEntry('Correlated log event 2', '2023-10-01T12:00:01')
]
write_correlated_logs('my-log-group', 'my-log-stream', '12345', log_entries)