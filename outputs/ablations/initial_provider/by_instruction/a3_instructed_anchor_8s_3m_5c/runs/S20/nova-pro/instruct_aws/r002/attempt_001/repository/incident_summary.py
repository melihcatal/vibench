import boto3
from observability_models import LogEvent

def summarize_error_logs(log_events: List[LogEvent]) -> str:
    error_logs = [log for log in log_events if 'ERROR' in log.message]
    return f'Found {len(error_logs)} error logs'

if __name__ == '__main__':
    log_events = [
        LogEvent(int(time.time() * 1000), 'INFO: Log message 1'),
        LogEvent(int(time.time() * 1000), 'ERROR: Log message 2'),
        LogEvent(int(time.time() * 1000), 'INFO: Log message 3')
    ]
    summary = summarize_error_logs(log_events)
    print(summary)