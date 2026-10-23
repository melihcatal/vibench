import boto3
import os


def metrics_export_archive(
    snapshot_data: str | bytes, bucket_name: str, object_key: str
):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    if isinstance(snapshot_data, str):
        snapshot_data = snapshot_data.encode("utf-8")
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=snapshot_data)
