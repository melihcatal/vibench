import os
import json
import boto3
from datetime import datetime

class LogClient:
    def __init__(self):
        self.logs_client = boto3.client(
            "logs",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

    def get_logs_client(self):
        return self.logs_client

def summarize_message_processing(log_group_name: str, log_stream_name: str, summary_data: dict):
    client = LogClient()
    logs_client = client.get_logs_client()

    try:
        # Ensure log group exists (optional, CloudWatch Logs can create on first put_log_events)
        # It's good practice to create it explicitly if it's a new log group
        try:
            logs_client.create_log_group(logGroupName=log_group_name)
        except logs_client.exceptions.ResourceAlreadyExistsException:
            pass

        # Ensure log stream exists (optional, CloudWatch Logs can create on first put_log_events)
        try:
            logs_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        except logs_client.exceptions.ResourceAlreadyExistsException:
            pass

        response = logs_client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': int(datetime.now().timestamp() * 1000),
                    'message': json.dumps(summary_data)
                },
            ]
        )
        print(f"Message summary logged successfully: {response.get('nextSequenceToken')}")
        return response
    except Exception as e:
        print(f"Error logging message summary: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    # Ensure AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and CLOUDWATCH_LOG_GROUP_NAME, CLOUDWATCH_LOG_STREAM_NAME are set as environment variables
    log_group = os.environ.get("CLOUDWATCH_LOG_GROUP_NAME", "message-processing-summary")
    log_stream = os.environ.get("CLOUDWATCH_LOG_STREAM_NAME", "daily-summary-" + datetime.now().strftime("%Y-%m-%d"))

    summary = {
        "processed_messages": 100,
        "failed_messages": 2,
        "success_rate": 98.0,
        "timestamp": datetime.now().isoformat()
    }

    summarize_message_processing(log_group, log_stream, summary)
