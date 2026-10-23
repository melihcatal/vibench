
import boto3

def list_objects_with_prefix(bucket_name: str, prefix: str):
    """
    Lists stored objects under a specified S3 bucket and prefix.

    Args:
        bucket_name: The name of the S3 bucket.
        prefix: The prefix to filter objects by.

    Returns:
        A list of object keys matching the prefix.
    """
    s3_client = boto3.client('s3')  # AWS S3 client
    objects = []
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in pages:
        if "Contents" in page:
            for obj in page["Contents"]:
                objects.append(obj["Key"])
    return objects
