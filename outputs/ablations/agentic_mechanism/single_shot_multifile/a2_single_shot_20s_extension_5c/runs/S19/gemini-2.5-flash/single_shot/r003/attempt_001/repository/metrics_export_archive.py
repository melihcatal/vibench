import os
import boto3

def archive_metric_snapshot(bucket_name: str, key: str, data: bytes) -> bool:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    )

    try:
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=data)
        return True
    except Exception as e:
        print(f"Error archiving to S3: {e}")
        return False