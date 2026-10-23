import boto3
from typing import List, Dict, Any, Optional
from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject

def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    """
    Lists stored objects under a bucket or container prefix in AWS S3.
    """
    s3_client = get_s3_client()
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(
            Bucket=request.bucket_name,
            Prefix=request.prefix,
            Delimiter=request.delimiter,
            MaxKeys=request.max_keys
        )

        objects: List[ListedObject] = []
        for page in pages:
            for obj in page.get('Contents', []):
                objects.append(
                    ListedObject(
                        key=obj.get('Key'),
                        last_modified=obj.get('LastModified').isoformat() if 'LastModified' in obj else None,
                        etag=obj.get('ETag', '').strip(''"'),
                        size=obj.get('Size'),
                        storage_class=obj.get('StorageClass')
                    )
                )
            for common_prefix in page.get('CommonPrefixes', []):
                objects.append(
                    ListedObject(
                        key=common_prefix.get('Prefix'),
                        is_prefix=True
                    )
                )

        return ListPrefixResponse(success=True, bucket_name=request.bucket_name, prefix=request.prefix, objects=objects)
    except Exception as e:
        return ListPrefixResponse(success=False, bucket_name=request.bucket_name, prefix=request.prefix, objects=[], message=f"Error listing objects: {e}")

