
import boto3
import datetime

def fetch_recent_logs(
    log_group_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    filter_pattern: str = ""
) -> list:
    """
    Retrieves recent log results from AWS CloudWatch Logs, filtered by field values and time range.

    Args:
        log_group_name: The name of the CloudWatch Log Group.
        start_time: The start of the time range to query.
        end_time: The end of the time range to query.
        filter_pattern: An optional CloudWatch Logs filter pattern to apply.

    Returns:
        A list of log events.
    """
    client = boto3.client("logs")  # AWS CloudWatch Logs client

    log_events = []
    next_token = None

    while True:
        if next_token:
            response = client.filter_log_events(
                logGroupName=log_group_name,
                startTime=int(start_time.timestamp() * 1000),
                endTime=int(end_time.timestamp() * 1000),
                filterPattern=filter_pattern,
                nextToken=next_token,
            )
        else:
            response = client.filter_log_events(
                logGroupName=log_group_name,
                startTime=int(start_time.timestamp() * 1000),
                endTime=int(end_time.timestamp() * 1000),
                filterPattern=filter_pattern,
            )

        log_events.extend(response["events"])

        next_token = response.get("nextToken")
        if not next_token:
            break

    return log_events
