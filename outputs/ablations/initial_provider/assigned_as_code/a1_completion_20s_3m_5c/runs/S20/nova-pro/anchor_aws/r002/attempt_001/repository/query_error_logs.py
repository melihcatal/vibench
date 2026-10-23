import boto3
import time


def query_error_logs(config, start_time, end_time):
    client = boto3.client("logs", region_name=config.get("region"))
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        startTime=int(start_time * 1000),
        endTime=int(end_time * 1000),
        filterPattern='ERROR',
    )
    return response["events"]