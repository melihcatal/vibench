import os
import json
import boto3
from typing import Dict

def archive_document_to_s3(record: Dict[str, any], bucket_name: str) -> bool:
    """
    Archives a document snapshot as a JSON file in an Amazon S3 bucket.

    Args:
        record: A dictionary representing the document record.
        bucket_name: The name of the S3 bucket to upload to.

    Returns:
        True if the upload was successful, False otherwise.
    """
    # boto3 will automatically use credentials from environment variables
    # (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN) or an IAM role.
    s3_client = boto3.client("s3")
    
    doc_id = record.get("_id")
    if not doc_id:
        print("Error: Record must have an '_id' to be archived.")
        return False
        
    object_key = f"archive/{doc_id}.json"
    
    try:
        # Convert the Python dictionary to a JSON string
        record_json_string = json.dumps(record, indent=4, default=str)
        
        # The put_object method uploads data to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=record_json_string,
            ContentType='application/json'
        )
        print(f"Successfully archived document '{doc_id}' to s3://{bucket_name}/{object_key}")
        return True
    except Exception as e:
        print(f"Failed to archive document '{doc_id}' to S3. Error: {e}")
        return False
