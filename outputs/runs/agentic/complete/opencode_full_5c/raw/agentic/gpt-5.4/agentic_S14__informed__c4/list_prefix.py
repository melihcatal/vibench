from __future__ import annotations

from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResult, normalize_s3_list


def list_prefix(request: ListPrefixRequest) -> ListPrefixResult:
    s3 = get_s3_client()
    params = {
        "Bucket": request.bucket,
        "Prefix": request.prefix,
        "MaxKeys": request.max_keys,
    }
    if request.continuation_token:
        params["ContinuationToken"] = request.continuation_token
    response = s3.list_objects_v2(**params)
    return normalize_s3_list(request.bucket, request.prefix, response)
