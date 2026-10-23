from storage_client import s3_config
from storage_models import parse_object_summary, ObjectSummary
from typing import List
import boto3


def list_objects(bucket: str, prefix: str = "") -> List[ObjectSummary]:
    client = boto3.client("s3", **s3_config)
    paginator = client.get_paginator("list_objects_v2")
    summaries: List[ObjectSummary] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if "Contents" in page:
            summaries.extend(parse_object_summary(c) for c in page["Contents"])
    return summaries
