from storage_client import get_s3_client
from storage_models import ListPrefixRequest, ListPrefixResponse, StorageObject


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    s3_client = get_s3_client()
    try:
        objects = []
        common_prefixes = []
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(
            Bucket=request.bucket_name, Prefix=request.prefix, MaxKeys=request.max_keys
        )

        for page in pages:
            for obj in page.get("Contents", []):
                objects.append(
                    StorageObject(
                        bucket_name=request.bucket_name,
                        key=obj.get("Key"),
                        last_modified=obj.get("LastModified"),
                        size=obj.get("Size"),
                        etag=obj.get("ETag", "").strip("\"'"),
                        storage_class=obj.get("StorageClass"),
                    )
                )
            for common_prefix_entry in page.get("CommonPrefixes", []):
                common_prefixes.append(common_prefix_entry.get("Prefix"))

        return ListPrefixResponse(
            bucket_name=request.bucket_name,
            prefix=request.prefix,
            objects=objects,
            common_prefixes=common_prefixes,
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to list objects with prefix {request.prefix} in {request.bucket_name}: {e}"
        )
