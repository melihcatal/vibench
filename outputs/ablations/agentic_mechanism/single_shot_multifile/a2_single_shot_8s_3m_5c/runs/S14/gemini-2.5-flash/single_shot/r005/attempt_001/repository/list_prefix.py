import os
from typing import List
from storage_client import get_s3_client, S3_BUCKET_NAME
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject

def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()
    listed_objects: List[ListedObject] = []
    continuation_token = None

    try:
        while True:
            list_kwargs = {
                'Bucket': S3_BUCKET_NAME,
                'Prefix': request.prefix,
                'MaxKeys': request.max_keys or 1000  # Default max_keys
            }
            if continuation_token:
                list_kwargs['ContinuationToken'] = continuation_token

            response = s3_client.list_objects_v2(**list_kwargs)

            for content in response.get('Contents', []):
                listed_objects.append(ListedObject(
                    object_key=content.get('Key'),
                    last_modified=content.get('LastModified').isoformat() if content.get('LastModified') else None,
                    size=content.get('Size')
                ))
            
            if not response.get('IsTruncated'):
                break
            continuation_token = response.get('NextContinuationToken')

        return ListPrefixResponse(success=True, prefix=request.prefix, objects=listed_objects)
    except Exception as e:
        return ListPrefixResponse(success=False, prefix=request.prefix, error_message=str(e))
