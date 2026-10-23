import os
from typing import Any, Dict

import boto3


def get_transcribe_client():
    region = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    return boto3.client("transcribe", region_name=region)


def get_s3_client():
    region = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    return boto3.client("s3", region_name=region)


def parse_transcribe_job(job: Dict[str, Any]) -> Dict[str, Any]:
    return dict(job)
