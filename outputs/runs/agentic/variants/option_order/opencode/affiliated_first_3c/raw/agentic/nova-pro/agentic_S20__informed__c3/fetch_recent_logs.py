import boto3
import os

client = boto3.client(
    "logs",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def fetch_logs(log_group, filter_pattern, start_time, end_time):
    response = client.filter_log_events(
        logGroupName=log_group,
        filterPattern=filter_pattern,
        startTime=start_time,
        endTime=end_time,
    )
    return response["events"]


log_group = "my-log-group"
filter_pattern = '[level = "ERROR"]'
start_time = int(round(time.time() * 1000)) - 3600000  # last hour
end_time = int(round(time.time() * 1000))

results = fetch_logs(log_group, filter_pattern, start_time, end_time)
for result in results:
    print(result)
