import os
import boto3

def archive_image_asset(file_content: bytes, bucket_name: str, object_name: str):
    s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION"))
    s3.put_object(Bucket=bucket_name, Key=object_name, Body=file_content)
    return f"s3://{bucket_name}/{object_name}"

def archive_text_asset(text_content: str, bucket_name: str, object_name: str):
    s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION"))
    s3.put_object(Bucket=bucket_name, Key=object_name, Body=text_content.encode('utf-8'))
    return f"s3://{bucket_name}/{object_name}"
