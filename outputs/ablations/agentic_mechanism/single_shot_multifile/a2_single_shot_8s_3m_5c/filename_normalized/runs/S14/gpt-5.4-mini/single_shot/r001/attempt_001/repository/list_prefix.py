from storage_client import get_s3_client, get_storage_config
from storage_models import ListPrefixRequest, ListPrefixResponse, normalize_list_response


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    config = get_storage_config()
    client = get_s3_client(config)
    paginator = client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=request.bucket, Prefix=request.prefix or "")
    return normalize_list_response(request.bucket, request.prefix or "", pages)
