import boto3
import os

def archive_record(record_id, content_bytes, bucket_name, object_key=None):
    s3_client = boto3.client('s3')
    
    if object_key is None:
        object_key = f"archives/{record_id}.json"

    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=content_bytes)
        return {"status": "success", "bucket": bucket_name, "key": object_key}
    except Exception as e:
        return {"status": "error", "message": str(e)}
