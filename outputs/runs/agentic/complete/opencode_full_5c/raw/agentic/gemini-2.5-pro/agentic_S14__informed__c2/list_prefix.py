from typing import List
from storage_client import get_storage_client
from storage_models import StoredObject
from botocore.exceptions import ClientError


def list_objects_by_prefix(bucket_name: str, prefix: str) -> List[StoredObject]:
    """
    Lists objects in an S3 bucket that start with a given prefix.
    """
    s3_client = get_storage_client()
    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        object_list = []
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    stored_obj = StoredObject(
                        key=obj["Key"],
                        size=obj["Size"],
                        last_modified=obj["LastModified"].isoformat(),
                    )
                    object_list.append(stored_obj)
        return object_list
    except ClientError as e:
        raise e
