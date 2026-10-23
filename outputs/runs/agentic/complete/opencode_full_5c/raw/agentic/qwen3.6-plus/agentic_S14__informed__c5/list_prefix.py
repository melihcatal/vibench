from storage_models import ListPrefixRequest, ObjectListingResponse, ObjectListingItem
from storage_client import get_storage_client, get_bucket, list_objects


def list_objects_by_prefix(bucket_name, prefix="", delimiter="", max_results=None):
    request = ListPrefixRequest(
        bucket=bucket_name,
        prefix=prefix,
        delimiter=delimiter,
        max_results=max_results,
    )
    client = get_storage_client()
    bucket = get_bucket(client, request.bucket)
    blobs = list_objects(
        bucket,
        prefix=request.prefix,
        delimiter=request.delimiter,
        max_results=request.max_results,
    )
    items = []
    for blob in blobs:
        items.append(
            ObjectListingItem(
                name=blob.name,
                size=blob.size,
                content_type=blob.content_type,
                last_modified=blob.updated,
                etag=blob.etag,
            )
        )
    prefixes = list(blobs.prefixes) if hasattr(blobs, "prefixes") else []
    return ObjectListingResponse(
        objects=items,
        prefixes=prefixes,
    )
