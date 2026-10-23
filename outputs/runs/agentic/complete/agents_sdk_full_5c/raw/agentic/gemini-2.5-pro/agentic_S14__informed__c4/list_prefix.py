import logging
from typing import List
from botocore.exceptions import ClientError
from storage_client import get_storage_client
from storage_models import ObjectSummary

# Provider: Amazon S3
# SDK: boto3

def list_objects_with_prefix(bucket_name: str, prefix: str = "") -> List[ObjectSummary]:
    """
    Lists objects in an S3 bucket under a given prefix.

    :param bucket_name: The name of the bucket.
    :param prefix: The prefix to filter objects by.
    :return: A list of ObjectSummary objects.
    """
    s3_client = get_storage_client()
    summaries = []
    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    summaries.append(
                        ObjectSummary(
                            key=obj["Key"],
                            size=obj["Size"],
                            last_modified=obj["LastModified"],
                        )
                    )
    except ClientError as e:
        logging.error(f"Could not list objects in bucket {bucket_name} with prefix '{prefix}': {e}")

    return summaries
