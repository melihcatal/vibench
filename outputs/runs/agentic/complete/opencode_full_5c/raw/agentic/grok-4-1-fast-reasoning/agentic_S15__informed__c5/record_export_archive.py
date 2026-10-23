import os
import boto3
import json
from typing import List
from database_models import Document


def archive_records(records: List[Document], archive_key: str):
    bucket = os.getenv("S3_BUCKET_NAME")
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
    data = json.dumps(records, default=str, indent=2)
    s3_client.put_object(
        Bucket=bucket, Key=archive_key, Body=data, ContentType="application/json"
    )
