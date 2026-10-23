import os
import boto3

# [LATER-STEP] metrics_export_archive.py


def metrics_export_archive(file_path):
    client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    with open(file_path, "rb") as file:
        client.upload_fileobj(file, "my-metrics-bucket", "metrics.json")
