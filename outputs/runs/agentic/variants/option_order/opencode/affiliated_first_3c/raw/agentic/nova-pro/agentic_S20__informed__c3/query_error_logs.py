import boto3
import os

client = boto3.client(
    "logs",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def query_logs(log_group, query, start_time, end_time):
    response = client.start_query(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
    )
    query_id = response["queryId"]
    while True:
        status = client.get_query_results(queryId=query_id)
        if status["status"] == "Complete":
            return status["results"]
        time.sleep(1)


log_group = "my-log-group"
query = "fields @message | sort @timestamp desc | limit 20"
start_time = int(round(time.time() * 1000)) - 3600000  # last hour
end_time = int(round(time.time() * 1000))

results = query_logs(log_group, query, start_time, end_time)
for result in results:
    print(result)
