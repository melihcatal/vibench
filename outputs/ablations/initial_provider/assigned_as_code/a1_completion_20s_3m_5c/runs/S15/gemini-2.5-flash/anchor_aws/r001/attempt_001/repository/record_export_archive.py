import os

import boto3


def archive_record_export(file_content: bytes, bucket_name: str, object_name: str, region_name: str = "us-east-1") -> dict:
    s3_client = boto3.client("s3", region_name=region_name)
    s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=file_content)
    return {"bucket": bucket_name, "object_name": object_name, "status": "archived"}
