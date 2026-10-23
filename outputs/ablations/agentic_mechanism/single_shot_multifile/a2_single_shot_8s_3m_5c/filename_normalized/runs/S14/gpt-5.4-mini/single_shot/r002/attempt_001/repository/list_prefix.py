from typing import List

from storage_client import get_s3_client, resolve_bucket_name
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    client = get_s3_client()
    bucket = resolve_bucket_name(request.bucket)
    paginator = client.get_paginator("list_objects_v2")
    items = []
    for page in paginator.paginate(Bucket=bucket, Prefix=request.prefix or "", Delimiter=request.delimiter or ""):
        for obj in page.get("Contents", []):
            items.append(
                ListedObject(
                    bucket=bucket,
                    key=obj["Key"],
                    size=obj.get("Size", 0),
                    last_modified=obj.get("LastModified"),
                    etag=obj.get("ETag", "").strip('"'),
                    storage_class=obj.get("StorageClass"),
                )
            )
    return ListPrefixResponse(bucket=bucket, prefix=request.prefix or "", objects=items)
