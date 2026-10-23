import os
import boto3


def metrics_export_archive(local_snapshot_path: str, bucket_name: str, object_key: str):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    s3_client.upload_file(local_snapshot_path, bucket_name, object_key)
