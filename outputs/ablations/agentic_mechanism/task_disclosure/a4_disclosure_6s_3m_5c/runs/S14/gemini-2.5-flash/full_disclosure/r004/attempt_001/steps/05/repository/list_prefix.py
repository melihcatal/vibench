import boto3

def list_objects_with_prefix(bucket_name: str, prefix: str) -> list[str]:
    """
    Lists stored objects under a specified S3 bucket and prefix.

    Args:
        bucket_name: The name of the S3 bucket.
        prefix: The prefix to filter objects by.

    Returns:
        A list of object keys matching the prefix.
    """
    s3 = boto3.client("s3")
    object_keys = []
    paginator = s3.get_paginator("list_objects_v2")

    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    for page in pages:
        if "Contents" in page:
            for obj in page["Contents"]:
                object_keys.append(obj["Key"])
    return object_keys
