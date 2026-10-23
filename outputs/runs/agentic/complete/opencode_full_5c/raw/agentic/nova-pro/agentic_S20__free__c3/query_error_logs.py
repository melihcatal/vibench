import boto3
import time

cw_logs = boto3.client("logs", region_name="us-west-2")

log_group_name = "MyLogGroup"


def query_error_logs(start_time, end_time):
    query = "fields @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20"
    response = cw_logs.start_query(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
    )
    query_id = response["queryId"]
    while True:
        status = cw_logs.get_query_results(queryId=query_id)
        if status["status"] == "Complete":
            return status["results"]
        time.sleep(1)


if __name__ == "__main__":
    start_time = int(time.time() * 1000) - 3600000  # 1 hour ago
    end_time = int(time.time() * 1000)
    results = query_error_logs(start_time, end_time)
    print(results)
