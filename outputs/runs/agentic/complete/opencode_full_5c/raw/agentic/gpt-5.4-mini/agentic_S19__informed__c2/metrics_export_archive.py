import os
from pathlib import Path

import boto3


def metrics_export_archive(file_path: str, bucket: str, key: str):
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket, key)
    return {"bucket": bucket, "key": key, "source": Path(file_path).name}
