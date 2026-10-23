from observability_client import ObservabilityClient
from observability_models import LogQueryResponse
import os
import time
from datetime import datetime, timedelta


def query_error_logs(
    log_group_name: str, duration_minutes: int = 60, severity_level: str = "ERROR"
) -> LogQueryResponse:
    client = ObservabilityClient()

    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int(
        (datetime.now() - timedelta(minutes=duration_minutes)).timestamp() * 1000
    )

    # CloudWatch Logs Insights query for error logs
    query_string = f'fields @timestamp, @message | filter @message like /"level":"{{severity_level}}"/ | sort @timestamp desc'
    # Use f-string formatting to inject the severity_level. The inner quotes need to be escaped.
    query_string = query_string.format(severity_level=severity_level)

    print(
        f"Starting query for '{severity_level}' logs in log group '{log_group_name}' for the last {duration_minutes} minutes..."
    )
    print(f"Query string: {query_string}")

    query_id = client.start_query(log_group_name, start_time, end_time, query_string)
    print(f"Query started with ID: {query_id}")

    status = "Running"
    events = []
    while status in ["Running", "Scheduled"]:
        time.sleep(1)  # Wait for 1 second before checking status again
        results = client.get_query_results(query_id)
        status = results["status"]
        print(f"Query status: {status}")

    if status == "Complete":
        for result in results["results"]:
            event = {}
            for field in result:
                event[field["field"]] = field["value"]
            events.append(event)
        print(f"Found {len(events)} {severity_level} log entries.")
    else:
        print(f"Query failed or cancelled with status: {status}")

    return LogQueryResponse(events)


if __name__ == "__main__":
    # Example usage: Ensure AWS_REGION environment variable and CLOUDWATCH_LOG_GROUP are set
    # Example: export AWS_REGION=us-east-1
    # Example: export CLOUDWATCH_LOG_GROUP=my-application-logs
    log_group = os.environ.get("CLOUDWATCH_LOG_GROUP", "my-application-logs")

    print("\nQuerying ERROR logs:")
    error_logs = query_error_logs(
        log_group_name=log_group, duration_minutes=120, severity_level="ERROR"
    )
    for log in error_logs.to_list():
        print(f"  Timestamp: {log.get('@timestamp')}, Message: {log.get('@message')}")

    print("\nQuerying INFO logs:")
    info_logs = query_error_logs(
        log_group_name=log_group, duration_minutes=120, severity_level="INFO"
    )
    for log in info_logs.to_list():
        print(f"  Timestamp: {log.get('@timestamp')}, Message: {log.get('@message')}")
