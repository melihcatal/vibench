import boto3
from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject

def list_objects_under_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_storage_client()
    try:
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(
            Bucket=request.bucket_name,
            Prefix=request.prefix
        )
        objects = []
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    objects.append(ListedObject(
                        object_key=obj['Key'],
                        size=obj['Size'],
                        last_modified=obj['LastModified'],
                        etag=obj['ETag']
                    ))
        return ListPrefixResponse(
            bucket_name=request.bucket_name,
            prefix=request.prefix,
            objects=objects,
            success=True
        )
    except Exception as e:
        return ListPrefixResponse(
            bucket_name=request.bucket_name,
            prefix=request.prefix,
            objects=[],
            success=False,
            error=str(e)
        )