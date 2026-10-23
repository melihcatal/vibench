import boto3
from datetime import datetime, timedelta

def fetch_recent_logs(log_group_name, start_time, end_time, filter_pattern=None):
    """
    Retrieves recent log results from AWS CloudWatch Logs.

    Args:
        log_group_name (str): The name of the log group.
        start_time (datetime): The start of the time range to query.
        end_time (datetime): The end of the time range to query.
        filter_pattern (str, optional): The filter pattern to apply. Defaults to None.

    Returns:
        list: A list of log events.
    """
    client = boto3.client('logs')

    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    params = {
        'logGroupName': log_group_name,
        'startTime': start_time_ms,
        'endTime': end_time_ms,
    }

    if filter_pattern:
        params['filterPattern'] = filter_pattern

    response = client.filter_log_events(**params)
    return response.get('events', [])

if __name__ == "__main__":
    # Example Usage:
    # Replace 'your-log-group-name' with the actual name of your CloudWatch Log Group
    # Ensure your AWS credentials are configured (e.g., via environment variables, AWS CLI, or IAM role)

    log_group = 'your-log-group-name' # e.g., '/aws/lambda/my-function'
    end = datetime.utcnow()
    start = end - timedelta(hours=1) # Last 1 hour

    print(f"Fetching logs from {log_group} between {start} and {end}...")

    # Fetch all logs
    all_recent_logs = fetch_recent_logs(log_group, start, end)
    print(f"Found {len(all_recent_logs)} total log events in the last hour.")
    # for event in all_recent_logs:
    #     print(f"[{datetime.fromtimestamp(event['timestamp']/1000)}] {event['message']}")

    # Fetch logs with a specific filter pattern (e.g., for errors)
    error_logs = fetch_recent_logs(log_group, start, end, filter_pattern='ERROR')
    print(f"Found {len(error_logs)} error log events in the last hour.")
    for event in error_logs:
        print(f"[{datetime.fromtimestamp(event['timestamp']/1000)}] {event['message']}")
