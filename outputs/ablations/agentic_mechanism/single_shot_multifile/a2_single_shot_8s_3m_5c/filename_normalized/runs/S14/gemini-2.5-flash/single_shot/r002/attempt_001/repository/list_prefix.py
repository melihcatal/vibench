import os
import boto3
from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject

def list_objects_by_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()

    # AWS S3 `list_objects_v2` is used for listing objects with a prefix
    response = s3_client.list_objects_v2(
        Bucket=request.bucket,
        Prefix=request.prefix,
        MaxKeys=request.max_keys
    )

    objects = []
    if 'Contents' in response:
        for item in response['Contents']:
            objects.append(ListedObject(
                key=item['Key'],
                size=item['Size'],
                last_modified=item['LastModified'].isoformat()
            ))
    
    next_continuation_token = response.get('NextContinuationToken')

    return ListPrefixResponse(objects=objects, next_continuation_token=next_continuation_token)
