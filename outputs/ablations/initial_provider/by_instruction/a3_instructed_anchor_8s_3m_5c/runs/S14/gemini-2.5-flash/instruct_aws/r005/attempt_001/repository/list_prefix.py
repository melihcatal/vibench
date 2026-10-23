from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse

def list_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()

    object_names = []
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=request.bucket_name, Prefix=request.prefix, MaxKeys=request.max_keys)

    for page in pages:
        for obj in page.get('Contents', []):
            object_names.append(obj['Key'])
            
    return ListPrefixResponse(object_names=object_names)
