import boto3
import datetime

def fetch_recent_logs(log_group_name, start_time, end_time, filter_pattern=None):
    """
    Retrieves recent log results from AWS CloudWatch Logs filtered by field values and time range.

    Args:
        log_group_name (str): The name of the CloudWatch Logs log group.
        start_time (datetime.datetime): The start of the time range to query.
        end_time (datetime.datetime): The end of the time range to query.
        filter_pattern (str, optional): The filter pattern to apply. Defaults to None.

    Returns:
        list: A list of log events.
    """
    client = boto3.client('logs')

    start_timestamp_ms = int(start_time.timestamp() * 1000)
    end_timestamp_ms = int(end_time.timestamp() * 1000)

    try:
        response = client.filter_log_events(
            logGroupName=log_group_name,
            startTime=start_timestamp_ms,
            endTime=end_timestamp_ms,
            filterPattern=filter_pattern,
            limit=1000  # Adjust as needed
        )
        return response['events']
    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

if __name__ == "__main__":
    # Example Usage:
    # Replace with your log group name and desired time range
    LOG_GROUP = "your-log-group-name"
    END_TIME = datetime.datetime.now(datetime.timezone.utc)
    START_TIME = END_TIME - datetime.timedelta(hours=1) # Last 1 hour

    # Optional: Filter pattern (e.g., "ERROR" or "{ $.level = "INFO" }")
    FILTER = None # Or 'ERROR' or '{ $.level = "INFO" }'

    print(f"Fetching logs from {LOG_GROUP} between {START_TIME} and {END_TIME}")
    if FILTER:
        print(f"With filter pattern: {FILTER}")

    logs = fetch_recent_logs(LOG_GROUP, START_TIME, END_TIME, FILTER)

    if logs:
        for event in logs:
            print(f"[{datetime.datetime.fromtimestamp(event['timestamp']/1000, datetime.timezone.utc)}] {event['message']}")
    else:
        print("No logs found.")
