import boto3


def query_error_logs(start_time, end_time):
    client = boto3.client("logs", region_name="us-west-2")
    response = client.filter_log_events(
        logGroupName="my-log-group",
        startTime=start_time,
        endTime=end_time,
        filterPattern="ERROR",
    )
    return response["events"]
