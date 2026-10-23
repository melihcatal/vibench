import boto3
import os

def archive_metric_snapshot(file_path: str, bucket_name: str, object_name: str):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, object_name)
