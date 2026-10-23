import boto3
import os
import uuid
import datetime

def write_correlated_log(log_group_name, log_stream_name, message, correlation_id):
    """
    Writes a log event to AWS CloudWatch Logs with a shared request or correlation identifier.
    """
    client = boto3.client('cloudwatchlogs')

    timestamp = int(datetime.datetime.now().timestamp() * 1000)

    log_event = {
        'timestamp': timestamp,
        'message': f"[{correlation_id}] {message}"
    }

    try:
        # Create log group and log stream if they don't exist
        try:
            client.create_log_group(logGroupName=log_group_name)
        except client.exceptions.ResourceAlreadyExistsException:
            pass

        try:
            client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        except client.exceptions.ResourceAlreadyExistsException:
            pass

        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[log_event]
        )
        print(f"Log event sent successfully: {response}")
    except Exception as e:
        print(f"Error sending log event: {e}")

if __name__ == "__main__":
    # Example usage:
    # Ensure AWS credentials are configured (e.g., via AWS CLI, environment variables)
    # export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
    # export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
    # export AWS_DEFAULT_REGION="YOUR_AWS_REGION" # e.g., us-east-1

    my_log_group = "my-application-logs"
    my_log_stream = "my-service-stream"
    
    # Generate a unique correlation ID for a request
    request_correlation_id = str(uuid.uuid4())

    print(f"Using Correlation ID: {request_correlation_id}")

    # Log events related to the same request
    write_correlated_log(my_log_group, my_log_stream, "User initiated login process.", request_correlation_id)
    write_correlated_log(my_log_group, my_log_stream, "Authentication successful for user 'test_user'.", request_correlation_id)
    write_correlated_log(my_log_group, my_log_stream, "Data fetched for dashboard.", request_correlation_id)
