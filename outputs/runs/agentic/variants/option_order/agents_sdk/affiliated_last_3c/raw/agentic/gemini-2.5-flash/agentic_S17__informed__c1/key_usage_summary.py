import os
import json
from datetime import datetime, timedelta
from security_client import get_cloudwatch_logs_client
from security_models import AuditEvent

def summarize_kms_key_usage(log_group_name: str, duration_hours: int = 24) -> dict:
    """
    Summarizes AWS KMS key usage and crypto events from CloudWatch Logs.
    Searches for CloudTrail logs related to KMS within a specified duration.
    """
    logs_client = get_cloudwatch_logs_client()
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=duration_hours)

    query = (
        "fields @timestamp, @message "
        "| filter eventSource = 'kms.amazonaws.com' "
        "| sort @timestamp desc"
    )

    try:
        start_query_response = logs_client.start_query(
            logGroupName=log_group_name,
            startTime=int(start_time.timestamp() * 1000),
            endTime=int(end_time.timestamp() * 1000),
            queryString=query,
            limit=1000 # Max number of log events to return
        )

        query_id = start_query_response['queryId']
        
        response = None
        while response is None or response['status'] == 'Running':
            # In a real application, you'd want to implement a delay here
            # For this example, we'll keep it simple.
            response = logs_client.get_query_results(queryId=query_id)
            if response['status'] == 'Complete':
                break

        events_summary = {}
        for result in response['results']:
            message_field = next((field['value'] for field in result if field['field'] == '@message'), None)
            if message_field:
                try:
                    event = AuditEvent.from_cloudtrail_event({"message": message_field})
                    event_name = event.event_name
                    if event_name not in events_summary:
                        events_summary[event_name] = []
                    events_summary[event_name].append(event.to_dict())
                except json.JSONDecodeError:
                    print(f"Could not parse log message: {message_field}")
        
        return events_summary

    except Exception as e:
        print(f"Error summarizing KMS key usage: {e}")
        raise

if __name__ == '__main__':
    # Example Usage
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME must be set.
    # CLOUDWATCH_LOG_GROUP_NAME should point to a log group receiving CloudTrail events.
    # Ensure CloudTrail is configured to send KMS events to a CloudWatch Logs group.
    log_group = os.environ.get("CLOUDWATCH_LOG_GROUP_NAME", "/aws/cloudtrail/my-trail")
    
    try:
        print(f"Summarizing KMS key usage for log group: {log_group}")
        summary = summarize_kms_key_usage(log_group, duration_hours=24)
        
        if summary:
            for event_name, events in summary.items():
                print(f"\nEvent Type: {event_name} ({len(events)} occurrences)")
                for event in events:
                    print(f"  - Event ID: {event['event_id']}, Time: {event['event_time']}, IP: {event['source_ip_address']}")
        else:
            print("No KMS usage events found in the specified duration.")

    except Exception as e:
        print(f"Failed to get KMS usage summary: {e}")
        print("Please ensure CloudTrail is configured to log KMS events to the specified CloudWatch Log Group.")
