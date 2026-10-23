import boto3
import json
import os
import datetime

def summarize_message_processing_result(message_id: str, status: str, details: dict):
    """
    Summarizes message processing results by logging them to AWS CloudWatch Logs.
    This function simulates sending a structured log event.
    """
    log_group_name = os.environ.get("AWS_CLOUDWATCH_LOG_GROUP", "/aws/message_processing_logs")
    log_stream_name = os.environ.get("AWS_CLOUDWATCH_LOG_STREAM", "message_summaries")
    
    # Initialize CloudWatch Logs client
    logs_client = boto3.client('logs')

    log_event = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "message_id": message_id,
        "status": status,
        "details": details
    }

    try:
        # Ensure log group and stream exist (idempotent operations)
        try:
            logs_client.create_log_group(logGroupName=log_group_name)
        except logs_client.exceptions.ResourceAlreadyExistsException:
            pass # Log group already exists
        
        try:
            logs_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        except logs_client.exceptions.ResourceAlreadyExistsException:
            pass # Log stream already exists

        # Get the sequence token for the put_log_events call
        response = logs_client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name
        )
        sequence_token = None
        if 'logStreams' in response and len(response['logStreams']) > 0:
            sequence_token = response['logStreams'][0].get('uploadSequenceToken')

        # Put the log event
        if sequence_token:
            put_response = logs_client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000),
                        'message': json.dumps(log_event)
                    },
                ],
                sequenceToken=sequence_token
            )
        else:
            put_response = logs_client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=[
                    {
                        'timestamp': int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000),
                        'message': json.dumps(log_event)
                    },
                ],
            )
        
        print(f"Log event for message {message_id} sent to CloudWatch Logs.")
        return put_response

    except Exception as e:
        print(f"Error sending log event to CloudWatch: {e}")
        raise

if __name__ == "__main__":
    summarize_message_processing_result(
        message_id="msg-summary-123", 
        status="completed", 
        details={
            "processor": "order_processor", 
            "duration_ms": 150,
            "items_processed": 5
        }
    )
