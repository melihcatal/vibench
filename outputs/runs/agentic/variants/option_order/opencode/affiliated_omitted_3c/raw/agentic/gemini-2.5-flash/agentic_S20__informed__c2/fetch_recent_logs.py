import os
import time
import datetime
import json

from observability_client import get_cloudwatch_logs_client
from observability_models import LogQuery, LogQueryResult


def fetch_recent_logs(
    log_group_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    filter_pattern: str = None,
):
    client = get_cloudwatch_logs_client()

    query_string = "fields @timestamp, @message"
    if filter_pattern:
        query_string += f" | filter {filter_pattern}"
    query_string += " | sort @timestamp desc | limit 20"

    start_query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=int(start_time.timestamp()),
        endTime=int(end_time.timestamp()),
        queryString=query_string,
        limit=20,
    )

    query_id = start_query_response["queryId"]
    print(f"Started CloudWatch Logs Insights query with ID: {query_id}")

    response = None
    while (
        response is None
        or response["status"] == "Running"
        or response["status"] == "Scheduled"
    ):
        print("Waiting for query to complete...")
        time.sleep(2)
        response = client.get_query_results(queryId=query_id)

    recent_logs = []
    if "results" in response:
        for result in response["results"]:
            timestamp_str = next(
                (field["value"] for field in result if field["field"] == "@timestamp"),
                None,
            )
            message_str = next(
                (field["value"] for field in result if field["field"] == "@message"),
                None,
            )

            if timestamp_str and message_str:
                # CloudWatch returns timestamp in 'YYYY-MM-DD HH:MM:SS.mmm' format
                try:
                    dt_object = datetime.datetime.strptime(
                        timestamp_str, "%Y-%m-%d %H:%M:%S.%f"
                    )
                except ValueError:
                    dt_object = datetime.datetime.strptime(
                        timestamp_str, "%Y-%m-%d %H:%M:%S"
                    )
                fields_dict = {field["field"]: field["value"] for field in result}
                recent_logs.append(
                    LogQueryResult(
                        timestamp=dt_object, message=message_str, fields=fields_dict
                    )
                )

    return recent_logs


if __name__ == "__main__":
    # Example Usage:
    log_group = os.environ.get("CLOUDWATCH_LOG_GROUP_NAME", "my-application-logs")

    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(hours=1)  # Last 1 hour

    # Example filter: logs where 'service' field is 'auth-service'
    # Or logs where the message contains 'User login'
    # filter_pattern = "service = 'auth-service'"
    filter_pattern = "message like /User login/"

    print(
        f"Fetching recent logs for log group: {log_group} with filter '{filter_pattern}' from {start_time} to {end_time}"
    )
    logs = fetch_recent_logs(log_group, start_time, end_time, filter_pattern)

    if logs:
        print("\n--- Recent Logs (filtered) ---")
        for log in logs:
            print(f"[{log.timestamp}] {log.message}")
            if log.fields:
                print(f"  Fields: {json.dumps(log.fields, indent=2)}")
    else:
        print("No recent logs found matching the filter in the specified time range.")
