import logging
from typing import List
from botocore.exceptions import ClientError
from storage_client import get_s3_client, get_storage_bucket
from storage_models import ListedObject

def list_objects_by_prefix(prefix: str, bucket_name: str = None) -> List[ListedObject]:
    """
    Lists objects in an S3 bucket that match a given prefix.

    :param prefix: The prefix to filter objects by.
    :param bucket_name: The S3 bucket. If None, uses default from env.
    :return: A list of ListedObject instances.
    """
    s3_client = get_s3_client()
    target_bucket = bucket_name or get_storage_bucket()
    results = []

    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=target_bucket, Prefix=prefix)

        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    results.append(
                        ListedObject(
                            key=obj["Key"],
                            size=obj["Size"],
                            last_modified=obj["LastModified"].isoformat()
                        )
                    )
    except ClientError as e:
        logging.error(f"Failed to list objects with prefix '{prefix}' in {target_bucket}: {e}")
        raise

    return results
