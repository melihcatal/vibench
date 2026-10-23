from observability_client import CLOUDWATCH_LOGS
from observability_models import LogEntry

def write_log(log_group, log_stream, log_entry):
    CLOUDWATCH_LOGS.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[log_entry.to_dict()]
    )

log_entry = LogEntry('Structured log event', '2023-10-01T12:00:00')
write_log('my-log-group', 'my-log-stream', log_entry)