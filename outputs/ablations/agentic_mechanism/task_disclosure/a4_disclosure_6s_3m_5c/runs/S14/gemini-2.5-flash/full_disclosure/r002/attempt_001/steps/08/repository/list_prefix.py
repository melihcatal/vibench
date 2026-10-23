import boto3

def list_objects_with_prefix(bucket_name, prefix):
    """
    Lists stored objects under a bucket or container prefix using AWS S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str): The prefix to filter the objects by.

    Returns:
        list: A list of object keys that match the given prefix.
    """
    s3_client = boto3.client('s3')
    objects = []
    paginator = s3_client.get_paginator('list_objects_v2')

    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    for page in pages:
        if "Contents" in page:
            for obj in page["Contents"]:
                objects.append(obj["Key"])
    return objects
