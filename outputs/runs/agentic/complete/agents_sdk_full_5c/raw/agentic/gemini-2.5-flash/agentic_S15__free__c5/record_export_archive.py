import boto3
import os
import json
from database_client import get_s3_client

def archive_document_snapshot(bucket_name: str, document_id: str, document_content: dict, folder_prefix: str = "archives"):
    """
    Archives exported document snapshots in AWS S3 managed object storage.
    The document_content is expected to be a dictionary (JSON serializable).
    """
    s3_client = get_s3_client()
    try:
        object_key = f"{folder_prefix}/{document_id}.json"
        document_bytes = json.dumps(document_content, indent=2).encode('utf-8')

        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=document_bytes,
            ContentType='application/json'
        )
        return {
            'bucket': bucket_name,
            'key': object_key,
            's3_response': response
        }
    except Exception as e:
        print(f"Error archiving document snapshot to S3: {e}")
        raise
