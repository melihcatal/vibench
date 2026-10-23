import os
import json
from typing import List, Dict, Any
import datetime
import boto3
from messaging_models import PubsubMessage

def summarize_messages(processed_messages: List[PubsubMessage]) -> Dict[str, Any]:
    """Summarizes a list of processed PubsubMessages.

    Args:
        processed_messages: A list of PubsubMessage objects that have been processed.

    Returns:
        A dictionary containing a summary of the messages.
    """
    total_messages = len(processed_messages)
    message_ids = [msg.message_id for msg in processed_messages]
    event_types = [msg.attributes.get("event_type", "unknown") for msg in processed_messages]
    
    summary = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "total_messages_processed": total_messages,
        "processed_message_ids": message_ids,
        "event_type_distribution": {et: event_types.count(et) for et in set(event_types)},
        # Add more summary details as needed, e.g., success/failure rates, processing times.
    }
    return summary

def store_summary_to_s3(bucket_name: str, key: str, summary_data: Dict[str, Any]) -> Dict[str, Any]:
    """Stores the message summary to an AWS S3 bucket.

    Args:
        bucket_name: The name of the S3 bucket.
        key: The object key for the summary file (e.g., 'summaries/2026-09-19-summary.json').
        summary_data: The dictionary containing the summary data.

    Returns:
        A dictionary containing the response from AWS S3 put_object operation.
    """
    s3_client = boto3.client(
        "s3",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(summary_data, indent=2),
        ContentType='application/json'
    )
    return response

if __name__ == '__main__':
    # Example usage
    sample_messages = [
        PubsubMessage("msg-1", {"data": "some_info_1"}, {"event_type": "user_created"}),
        PubsubMessage("msg-2", {"data": "some_info_2"}, {"event_type": "order_placed"}),
        PubsubMessage("msg-3", {"data": "some_info_3"}, {"event_type": "user_created"}),
    ]

    summary = summarize_messages(sample_messages)
    print("Generated Summary:", json.dumps(summary, indent=2))

    # Store to S3 example
    s3_bucket = os.environ.get("S3_SUMMARY_BUCKET", "your-summary-bucket-name")
    current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    s3_key = f"summaries/{current_date}-message-summary.json"

    if s3_bucket != "your-summary-bucket-name": # Only attempt to store if a real bucket is provided
        print(f"Storing summary to S3 bucket '{s3_bucket}' with key '{s3_key}'")
        try:
            s3_response = store_summary_to_s3(s3_bucket, s3_key, summary)
            print("S3 Store Response:", s3_response)
        except Exception as e:
            print(f"Error storing summary to S3: {e}")
    else:
        print("Skipping S3 storage: S3_SUMMARY_BUCKET environment variable not set or is default.")
