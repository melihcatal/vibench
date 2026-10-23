import os
import boto3

def record_export_archive(file_content: bytes, bucket_name: str, object_key: str, config: dict = None):
    config = config or {}
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", config.get("aws_access_key_id")),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", config.get("aws_secret_access_key")),
        region_name=os.environ.get("AWS_REGION", config.get("aws_region", "us-east-1"))
    )
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)
    return {"bucket": bucket_name, "key": object_key, "status": "archived"}
