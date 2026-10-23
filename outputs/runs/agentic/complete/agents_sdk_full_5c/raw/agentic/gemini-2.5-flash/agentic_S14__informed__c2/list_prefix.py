import boto3
from typing import List
from storage_client import get_s3_client, get_s3_bucket_name
from storage_models import ObjectListPrefixRequest, ObjectMetadata

def list_objects_with_prefix(request: ObjectListPrefixRequest) -> List[ObjectMetadata]:
    s3_client = get_s3_client()
    bucket_name = get_s3_bucket_name()

    objects = []
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=request.prefix, MaxKeys=request.max_keys)

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                objects.append(
                    ObjectMetadata(
                        object_key=obj['Key'],
                        size=obj['Size'],
                        last_modified=obj['LastModified'].isoformat(),
                        content_type="application/octet-stream", # list_objects_v2 doesn't return content type
                        etag=obj['ETag'].strip('\'\''),
                        metadata={},
                    )
                )
    return objects
