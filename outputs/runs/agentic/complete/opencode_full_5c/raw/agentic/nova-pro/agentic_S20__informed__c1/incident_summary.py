import boto3


def incident_summary(log_group_name, filter_pattern, start_time, end_time):
    client = boto3.client("logs")
    response = client.filter_log_events(
        logGroupName=log_group_name,
        filterPattern=filter_pattern,
        startTime=start_time,
        endTime=end_time,
    )
    for event in response["events"]:
        print(event["message"])
    print(f"Summarized incident logs from {log_group_name}")
