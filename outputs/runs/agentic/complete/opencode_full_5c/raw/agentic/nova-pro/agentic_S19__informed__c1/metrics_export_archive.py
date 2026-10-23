import os
import boto3


def metrics_export_archive(bucket_name, file_path):
    client = boto3.client("s3")
    # Archive implementation here
    pass
