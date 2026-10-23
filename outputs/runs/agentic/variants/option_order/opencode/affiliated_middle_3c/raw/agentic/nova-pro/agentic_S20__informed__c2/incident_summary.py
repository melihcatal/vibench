import boto3


def summarize_error_logs(log_group, start_time, end_time):
    client = boto3.client("logs", region_name="us-west-2")
    response = client.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        filterPattern="ERROR",
    )
    error_messages = [event["message"] for event in response["events"]]
    return " ".join(error_messages)
