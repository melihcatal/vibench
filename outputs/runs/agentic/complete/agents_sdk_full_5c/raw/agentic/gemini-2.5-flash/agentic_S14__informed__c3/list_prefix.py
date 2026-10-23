import os
from typing import List, Optional
from storage_client import get_s3_client
from storage_models import ObjectMetadata, ObjectListing

def list_objects_by_prefix(
    bucket_name: str,
    prefix: str = '',
    max_keys: int = 1000,
    continuation_token: Optional[str] = None
) -> ObjectListing:
    """
    Lists stored objects under a specified bucket prefix in Amazon S3.

    Args:
        bucket_name: The name of the S3 bucket.
        prefix: The prefix to filter objects by (e.g., 'myfolder/').
        max_keys: The maximum number of objects to return in a single call.
        continuation_token: Token for paginated results.

    Returns:
        An ObjectListing instance containing a list of ObjectMetadata objects
        and an optional continuation token for the next page.
    """
    s3_client = get_s3_client()

    list_params = {
        'Bucket': bucket_name,
        'Prefix': prefix,
        'MaxKeys': max_keys
    }
    if continuation_token:
        list_params['ContinuationToken'] = continuation_token

    try:
        response = s3_client.list_objects_v2(**list_params)

        objects: List[ObjectMetadata] = []
        if 'Contents' in response:
            for obj in response['Contents']:
                objects.append(
                    ObjectMetadata(
                        key=obj['Key'],
                        size=obj['Size'],
                        last_modified=obj['LastModified'].isoformat(),
                        e_tag=obj['ETag'].strip('\"')
                    )
                )
        
        next_token = response.get('NextContinuationToken')
        return ObjectListing(objects=objects, next_continuation_token=next_token)

    except Exception as e:
        print(f"Error listing objects by prefix: {e}")
        raise
