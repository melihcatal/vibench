from observability_client import ObservabilityClient
from observability_models import LogQueryResponse
import os
from datetime import datetime, timedelta


def fetch_recent_logs(
    log_group_name: str, duration_minutes: int = 60, filter_pattern: str = ""
) -> LogQueryResponse:
    client = ObservabilityClient()

    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int(
        (datetime.now() - timedelta(minutes=duration_minutes)).timestamp() * 1000
    )

    print(
        f"Fetching recent logs from log group '{log_group_name}' for the last {duration_minutes} minutes with filter pattern: '{filter_pattern}'"
    )

    events = client.filter_log_events(
        log_group_name=log_group_name,
        start_time=start_time,
        end_time=end_time,
        filter_pattern=filter_pattern,
    )

    print(f"Found {len(events)} recent log entries.")
    return LogQueryResponse(events)


if __name__ == "__main__":
    # Example usage: Ensure AWS_REGION environment variable and CLOUDWATCH_LOG_GROUP are set
    # Example: export AWS_REGION=us-east-1
    # Example: export CLOUDWATCH_LOG_GROUP=my-application-logs
    log_group = os.environ.get("CLOUDWATCH_LOG_GROUP", "my-application-logs")

    print("\nFetching all recent logs:")
    all_logs = fetch_recent_logs(log_group_name=log_group, duration_minutes=60)
    for log in all_logs.to_list():
        print(f"  Timestamp: {log.get('timestamp')}, Message: {log.get('message')}")

    print("\nFetching recent logs containing 'User logged in':")
    user_login_logs = fetch_recent_logs(
        log_group_name=log_group,
        duration_minutes=60,
        filter_pattern='{ ($.level = "INFO" || $.level = "ERROR") && $.message like /User logged in/ }',
    )
    for log in user_login_logs.to_list():
        print(f"  Timestamp: {log.get('timestamp')}, Message: {log.get('message')}")

    print("\nFetching recent logs with correlation_id 'req-abc-123':")
    correlated_logs = fetch_recent_logs(
        log_group_name=log_group,
        duration_minutes=60,
        filter_pattern='{ $.correlation_id = "req-abc-123" }',
    )
    for log in correlated_logs.to_list():
        print(f"  Timestamp: {log.get('timestamp')}, Message: {log.get('message')}")
