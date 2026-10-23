import os
import boto3
import json
from datetime import datetime

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AUDIT_LOG_GROUP_NAME = os.environ.get("AUDIT_LOG_GROUP_NAME", "/aws/identity/federated-login-audits")

def summarize_audit_events(start_time_ms: int, end_time_ms: int, filter_pattern: str = ""):
    """
    Summarizes federated-login audit events from AWS CloudWatch Logs.
    """
    client = boto3.client("logs", region_name=AWS_REGION)

    try:
        response = client.filter_log_events(
            logGroupName=AUDIT_LOG_GROUP_NAME,
            startTime=start_time_ms,
            endTime=end_time_ms,
            filterPattern=filter_pattern,
            limit=100  # Limit to 100 events for a summary
        )

        summary = {
            "event_count": len(response.get("events", [])),
            "events": []
        }

        for event in response.get("events", []):
            message = event.get("message")
            timestamp = event.get("timestamp")
            try:
                event_data = json.loads(message)
                summary["events"].append({
                    "timestamp": datetime.fromtimestamp(timestamp / 1000).isoformat(),
                    "user_id": event_data.get("user_id"),
                    "event_type": event_data.get("event_type"),
                    "status": event_data.get("status"),
                    "details": event_data.get("details", {})
                })
            except json.JSONDecodeError:
                summary["events"].append({
                    "timestamp": datetime.fromtimestamp(timestamp / 1000).isoformat(),
                    "raw_message": message
                })

        return summary

    except client.exceptions.ResourceNotFoundException:
        print(f"Log group '{AUDIT_LOG_GROUP_NAME}' not found.")
        return {"event_count": 0, "events": []}
    except Exception as e:
        print(f"Error summarizing audit events: {e}")
        raise

if __name__ == "__main__":
    # Example usage: last 24 hours
    end = int(datetime.now().timestamp() * 1000)
    start = int((datetime.now().timestamp() - 24 * 3600) * 1000)

    try:
        audit_summary = summarize_audit_events(start, end, filter_pattern="{ $.event_type = 'LOGIN' || $.event_type = 'LOGOUT' }")
        print("Federated Login Audit Summary:")
        print(json.dumps(audit_summary, indent=2))
    except Exception as e:
        print(f"An error occurred: {e}")
