import boto3
from observability_client import get_logs_client
from observability_models import LogResponse

def summarize_error_logs(log_group, start_time, end_time):
    client = get_logs_client()
    response = client.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        filterPattern='severity:ERROR'
    )
    events = LogResponse(**response).events
    summary = {
        'total_errors': len(events),
        'error_types': {}
    }
    for event in events:
        error_type = event.message.get('event')
        if error_type in summary['error_types']:
            summary['error_types'][error_type] += 1
        else:
            summary['error_types'][error_type] = 1
    return summary

if __name__ == '__main__':
    summary = summarize_error_logs('my-log-group', 1609459200000, 1612137600000)
    print(summary)
