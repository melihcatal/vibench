import os
import boto3
from datetime import datetime, timedelta

def summarize_login_audit_events(log_group_name: str, start_time_minutes_ago: int = 60) -> list[dict]:
    """
    Summarizes federated-login audit events from AWS CloudWatch Logs.
    Fetches log events for a specified log group within a time window.
    """
    client = boto3.client('logs')

    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=start_time_minutes_ago)

    response = client.filter_log_events(
        logGroupName=log_group_name,
        startTime=int(start_time.timestamp() * 1000), # Milliseconds
        endTime=int(end_time.timestamp() * 1000),
        # filterPattern="{ $.event_type = \"federated_login\" }" # Example filter
        limit=100 # Limit to 100 events for summary
    )

    # In a real scenario, you would parse and summarize these events more meaningfully.
    # For this example, we just return the events.
    summarized_events = []
    for event in response.get('events', []):
        summarized_events.append({
            "event_id": event.get('eventId'),
            "timestamp": datetime.fromtimestamp(event.get('timestamp') / 1000).isoformat(),
            "message": event.get('message')
        })

    return summarized_events

if __name__ == 'main':
    # Example usage:
    # cloudwatch_log_group = os.environ.get("CLOUDWATCH_LOGIN_AUDIT_LOG_GROUP")
    # if cloudwatch_log_group:
    #     audit_summary = summarize_login_audit_events(cloudwatch_log_group, start_time_minutes_ago=10)
    #     print(f"Last 10 minutes login audit summary ({len(audit_summary)} events):")
    #     for event in audit_summary:
    #         print(f"  [{event['timestamp']}] {event['message']}")
    # else:
    #     print("Please set CLOUDWATCH_LOGIN_AUDIT_LOG_GROUP environment variable.")
    pass
