import os
import boto3


def record_export_archive(snapshot, key):
    client = boto3.client("s3")
    bucket = os.environ["AWS_S3_BUCKET"]
    client.put_object(Bucket=bucket, Key=key, Body=snapshot if isinstance(snapshot, (bytes, bytearray)) else str(snapshot).encode())
    return {"bucket": bucket, "key": key}
