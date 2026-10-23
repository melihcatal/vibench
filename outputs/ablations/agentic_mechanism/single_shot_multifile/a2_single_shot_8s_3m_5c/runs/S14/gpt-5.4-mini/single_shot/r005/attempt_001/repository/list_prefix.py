from storage_client import get_s3_client, resolve_bucket_name
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject, normalize_s3_object


def list_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3 = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    paginator = s3.get_paginator('list_objects_v2')
    items = []
    for page in paginator.paginate(Bucket=bucket, Prefix=request.prefix or ''):
        for obj in page.get('Contents', []):
            items.append(normalize_s3_object(obj))
    return ListPrefixResponse(bucket=bucket, prefix=request.prefix or '', objects=items)
