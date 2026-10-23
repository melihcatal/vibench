from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse
from typing import List

def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    """Lists stored objects under a bucket or container prefix in AWS S3.

    Args:
        request: A ListPrefixRequest containing bucket name, prefix, and max keys.

    Returns:
        A ListPrefixResponse with a list of object keys.
    """
    s3_client = get_s3_client()

    object_keys: List[str] = []
    paginator = s3_client.get_paginator('list_objects_v2')

    pages = paginator.paginate(
        Bucket=request.bucket_name,
        Prefix=request.prefix,
        MaxKeys=request.max_keys
    )

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                object_keys.append(obj['Key'])

    return ListPrefixResponse(object_keys=object_keys)
