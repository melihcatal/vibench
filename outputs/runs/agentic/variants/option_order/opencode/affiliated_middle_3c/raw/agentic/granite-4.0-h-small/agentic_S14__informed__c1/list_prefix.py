import boto3
from storage_client import get_s3_client


def list_objects_by_prefix(bucket_name, prefix, delimiter=None):
    """List objects under a bucket with a given prefix (folder-like listing).

    Uses the boto3 client from storage_client.get_s3_client(), configured with
    AWS credentials from the environment.
    """
    s3 = get_s3_client()
    paginator = s3.get_paginator("list_objects_v2")
    results = []
    for page in paginator.paginate(
        Bucket=bucket_name, Prefix=prefix, Delimiter=delimiter
    ):
        if "Contents" in page:
            results.extend(page["Contents"])
        if "CommonPrefixes" in page:
            results.extend(page["CommonPrefixes"])
    return results
