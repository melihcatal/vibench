# list_prefix.py
# [SAME-SCENARIO] Lists objects under a bucket/container prefix (Amazon S3 example)

import os
import boto3
from storage_client import create_s3_client


def list_objects_prefix(
    bucket: str, prefix: str = "", delimiter: str = None, max_keys: int = 1000
):
    """Lists objects under a bucket with the given prefix.
    Args:
        bucket (str): Bucket name.
        prefix (str): Prefix to filter object keys (default '').
        delimiter (str): Optional delimiter to simulate folder structure.
        max_keys (int): Max number of keys to return.
    Yields:
        dict: Each object's metadata (Key, LastModified, Size, etc.)
    """
    s3 = create_s3_client()
    kwargs = {"Bucket": bucket, "Prefix": prefix, "MaxKeys": max_keys}
    if delimiter:
        kwargs["Delimiter"] = delimiter
    # Pagination loop
    while True:
        response = s3.list_objects_v2(**kwargs)
        for obj in response.get("Contents", []):
            yield obj
        # If truncated, continue with NextContinuationToken
        if not response.get("IsTruncated"):
            break
        kwargs["ContinuationToken"] = response["NextContinuationToken"]


# Example usage (uncomment to test)
# for obj in list_objects_prefix('my-bucket', prefix='images/'):
#     print(obj['Key'], obj['Size'])
