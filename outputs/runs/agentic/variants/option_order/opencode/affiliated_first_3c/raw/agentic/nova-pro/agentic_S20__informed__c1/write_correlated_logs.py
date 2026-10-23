import boto3


def write_correlated_logs(log_group, log_stream, correlation_id, log_events):
    client = boto3.client("logs")
    for log_event in log_events:
        log_event["message"] = f"{correlation_id} {log_event['message']}"
    client.put_log_events(
        logGroupName=log_group, logStreamName=log_stream, logEvents=log_events
    )
