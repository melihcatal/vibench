import os
import boto3
from botocore.exceptions import ClientError


def list_objects_prefix(bucket_name, prefix, max_keys=1000):
    """List objects under a given prefix in an Amazon S3 bucket.

    Uses boto3 (AWS SDK), identifying the provider as Amazon S3.
    """
    s3 = boto3.client("s3")
    try:
        paginator = s3.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(
            Bucket=bucket_name, Prefix=prefix, PaginationConfig={"MaxKeys": max_keys}
        )
        objects = []
        for page in page_iterator:
            if "Contents" in page:
                objects.extend(page["Contents"])
        return objects
    except ClientError as e:
        print("Error listing objects:", e)
        return []
