from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)

    blobs = client.list_blobs(
        bucket, prefix=request.prefix, delimiter=request.delimiter
    )

    objects = []
    for blob in blobs:
        objects.append(
            {
                "name": blob.name,
                "size": blob.size,
                "content_type": blob.content_type,
                "last_modified": blob.updated.isoformat(),
            }
        )

    # Handle prefixes (directories) if a delimiter is used
    if request.delimiter:
        for prefix in blobs.prefixes:
            objects.append({"name": prefix, "is_prefix": True})

    return ListPrefixResponse(bucket_name=request.bucket_name, objects=objects)
