from typing import List
from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListedObject


def list_objects_with_prefix(request: ListPrefixRequest) -> List[ListedObject]:
    """
    Lists objects in an S3 bucket under a given prefix.
    """
    s3_client = get_storage_client()
    paginator = s3_client.get_paginator("list_objects_v2")

    pages = paginator.paginate(Bucket=request.bucket, Prefix=request.prefix)

    object_list = []
    for page in pages:
        if "Contents" in page:
            for obj in page["Contents"]:
                object_list.append(
                    ListedObject(
                        key=obj["Key"],
                        size=obj["Size"],
                        last_modified=obj["LastModified"].isoformat(),
                    )
                )

    return object_list
