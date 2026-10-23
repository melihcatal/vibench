import os
import time
import datetime

from observability_client import get_cloudwatch_logs_client
from observability_models import LogQuery, LogQueryResult


def query_error_logs(
    log_group_name: str, start_time: datetime.datetime, end_time: datetime.datetime
):
    client = get_cloudwatch_logs_client()

    # CloudWatch Logs Insights query for error logs
    query_string = "fields @timestamp, @message | filter level = 'ERROR' or message like /error/i | sort @timestamp desc | limit 20"

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

    error_logs = []
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
                error_logs.append(
                    LogQueryResult(
                        timestamp=dt_object, message=message_str, fields=fields_dict
                    )
                )

    return error_logs


if __name__ == "__main__":
    # Example Usage:
    log_group = os.environ.get("CLOUDWATCH_LOG_GROUP_NAME", "my-application-logs")

    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(hours=1)  # Last 1 hour

    print(
        f"Querying error logs for log group: {log_group} from {start_time} to {end_time}"
    )
    errors = query_error_logs(log_group, start_time, end_time)

    if errors:
        print("\n--- Recent Error Logs ---")
        for error in errors:
            print(f"[{error.timestamp}] {error.message}")
            if error.fields:
                print(f"  Fields: {json.dumps(error.fields, indent=2)}")
    else:
        print("No error logs found in the specified time range.")
