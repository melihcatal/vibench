import os
import boto3
from botocore.exceptions import ClientError


def archive_document_snapshot(bucket_name: str, object_name: str, content: bytes):
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=content)
        return True
    except ClientError:
        return False
