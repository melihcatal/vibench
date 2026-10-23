from __future__ import annotations

from storage_client import get_s3_bucket, get_s3_client
from storage_models import (
    ListPrefixRequest,
    ListPrefixResponse,
    ListedObject,
    normalize_datetime,
)


def list_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    client = get_s3_client()
    bucket = get_s3_bucket(request.bucket)
    response = (
        client.list_objects_v2(
            Bucket=bucket,
            Prefix=request.prefix,
            MaxKeys=request.max_keys,
            ContinuationToken=request.continuation_token,
        )
        if request.continuation_token
        else client.list_objects_v2(
            Bucket=bucket,
            Prefix=request.prefix,
            MaxKeys=request.max_keys,
        )
    )
    objects = [
        ListedObject(
            object_key=item["Key"],
            size=item.get("Size", 0),
            etag=item.get("ETag"),
            last_modified=normalize_datetime(item.get("LastModified")),
        )
        for item in response.get("Contents", [])
    ]
    return ListPrefixResponse(
        bucket=bucket,
        prefix=request.prefix,
        objects=objects,
        next_continuation_token=response.get("NextContinuationToken"),
    )
