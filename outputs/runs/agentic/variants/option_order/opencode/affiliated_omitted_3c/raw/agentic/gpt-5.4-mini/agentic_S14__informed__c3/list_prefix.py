from typing import List, Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import ListedObject, ListPrefixResponse, normalize_timestamp


def list_objects_with_prefix(prefix: str = '', bucket: Optional[str] = None, delimiter: Optional[str] = None) -> ListPrefixResponse:
    bucket_name = bucket or get_bucket_name()
    client = get_s3_client()
    params = {'Bucket': bucket_name, 'Prefix': prefix}
    if delimiter is not None:
        params['Delimiter'] = delimiter
    response = client.list_objects_v2(**params)
    items: List[ListedObject] = []
    for obj in response.get('Contents', []):
        items.append(ListedObject(key=obj.get('Key', ''), size=obj.get('Size', 0), last_modified=normalize_timestamp(obj.get('LastModified')), etag=obj.get('ETag'))) 
    return ListPrefixResponse(bucket=bucket_name, prefix=prefix, objects=items, is_truncated=response.get('IsTruncated', False), next_continuation_token=response.get('NextContinuationToken'))
