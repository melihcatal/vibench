import boto3
import os
from datetime import datetime, timedelta

def summarize_federated_login_audit_events(
    log_group_name: str,
    start_time: datetime = None,
    end_time: datetime = None
) -> dict:
    """
    Summarizes federated-login audit events from AWS CloudWatch Logs.

    Args:
        log_group_name: The name of the CloudWatch Log Group to query.
        start_time: The start time for filtering events (inclusive). Defaults to 24 hours ago.
        end_time: The end time for filtering events (exclusive). Defaults to now.

    Returns:
        A dictionary containing a summary of the audit events.
    """
    
    # AWS specific client for CloudWatch Logs
    # Provider-identifying signal: boto3.client('logs')
    client = boto3.client(
        'logs',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    if start_time is None:
        start_time = datetime.utcnow() - timedelta(days=1)
    if end_time is None:
        end_time = datetime.utcnow()

    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    all_events = []
    next_token = None

    while True:
        try:
            if next_token:
                response = client.filter_log_events(
                    logGroupName=log_group_name,
                    startTime=start_time_ms,
                    endTime=end_time_ms,
                    nextToken=next_token
                )
            else:
                response = client.filter_log_events(
                    logGroupName=log_group_name,
                    startTime=start_time_ms,
                    endTime=end_time_ms
                )
            
            all_events.extend(response.get('events', []))
            next_token = response.get('nextToken')

            if not next_token:
                break
        except client.exceptions.ResourceNotFoundException:
            return {"error": f"Log group '{log_group_name}' not found."}
        except Exception as e:
            return {"error": f"An AWS error occurred: {str(e)}"}

    total_events = len(all_events)
    summary = {
        "total_events": total_events,
        "first_event_timestamp": None,
        "last_event_timestamp": None,
        "event_types_count": {}
    }

    if total_events > 0:
        # Sort events by timestamp to find first and last
        sorted_events = sorted(all_events, key=lambda x: x['timestamp'])
        summary["first_event_timestamp"] = datetime.fromtimestamp(sorted_events[0]['timestamp'] / 1000).isoformat()
        summary["last_event_timestamp"] = datetime.fromtimestamp(sorted_events[-1]['timestamp'] / 1000).isoformat()

        # Simple categorization by message content (can be improved with more complex parsing)
        for event in all_events:
            message = event['message']
            # Example: Categorize based on keywords in the message
            if "login success" in message.lower():
                summary["event_types_count"]["login_success"] = summary["event_types_count"].get("login_success", 0) + 1
            elif "login failed" in message.lower():
                summary["event_types_count"]["login_failed"] = summary["event_types_count"].get("login_failed", 0) + 1
            else:
                summary["event_types_count"]["other"] = summary["event_types_count"].get("other", 0) + 1

    return summary
