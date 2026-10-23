import os
import boto3
from storage_client import get_s3_client


def list_objects_v2_prefix(bucket_name, prefix="", delimiter="/", max_keys=1000):
    """List objects under a bucket prefix using Amazon S3 List Objects V2 API.

    Authenticates via AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY.
    Returns a list of dictionaries for each object found.
    """
    s3_client = get_s3_client()
    paginator = s3_client.get_paginator("list_objects_v2")
    results = []
    for page in paginator.paginate(
        Bucket=bucket_name,
        Prefix=prefix,
        Delimiter=delimiter,
        PaginationConfig={"PageSize": max_keys},
    ):
        if "Contents" in page:
            results.extend(page["Contents"])
    return results
