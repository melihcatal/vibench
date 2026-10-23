
import boto3
import os
from datetime import datetime, timedelta

def get_cloudwatch_error_logs(log_group_name, duration_minutes=60):
    client = boto3.client('logs')
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)
    
    # CloudWatch Logs expects time in milliseconds
    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)
    
    error_logs = []
    paginator = client.get_paginator('filter_log_events')
    
    # Filter for events containing "ERROR" or "EXCEPTION"
    response_iterator = paginator.paginate(
        logGroupName=log_group_name,
        startTime=start_time_ms,
        endTime=end_time_ms,
        filterPattern='?ERROR ?EXCEPTION' 
    )
    
    for response in response_iterator:
        for event in response['events']:
            error_logs.append(event['message'])
            
    return error_logs

def summarize_incident_logs(log_group_name="MyApplicationLogGroup", duration_minutes=60):
    print(f"Fetching error logs from AWS CloudWatch Log Group: {log_group_name} for the last {duration_minutes} minutes...")
    
    error_messages = get_cloudwatch_error_logs(log_group_name, duration_minutes)
    
    if not error_messages:
        print("No error logs found for the specified period.")
        return

    summary = {
        "total_errors": len(error_messages),
        "unique_errors": len(set(error_messages)),
        "error_samples": error_messages[:5]  # Display up to 5 unique error samples
    }
    
    print("\n--- Incident Summary ---")
    print(f"Total error events: {summary['total_errors']}")
    print(f"Unique error messages: {summary['unique_errors']}")
    print("\nSample Error Messages:")
    for i, msg in enumerate(summary['error_samples']):
        print(f"{i+1}. {msg}")
    
    print("\n--- End Summary ---")

if __name__ == "__main__":
    # Ensure AWS credentials are configured (e.g., via AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION environment variables or ~/.aws/credentials)
    # Replace 'MyApplicationLogGroup' with your actual CloudWatch Log Group name
    # You can also adjust the duration_minutes as needed
    summarize_incident_logs(log_group_name=os.environ.get("CLOUDWATCH_LOG_GROUP_NAME", "MyApplicationLogGroup"), duration_minutes=60)
