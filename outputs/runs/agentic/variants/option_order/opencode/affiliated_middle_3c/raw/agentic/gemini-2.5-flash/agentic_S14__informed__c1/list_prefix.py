from storage_client import get_storage_client
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    """
    Lists stored objects under a Google Cloud Storage bucket or container prefix.
    """
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)

    objects = []
    prefixes = set()

    for blob in client.list_blobs(
        bucket, prefix=request.prefix, delimiter=request.delimiter
    ):
        if blob.name.endswith("/") and blob.name != request.prefix:
            prefixes.add(blob.name)
        else:
            objects.append(
                ListedObject(
                    object_name=blob.name,
                    size=blob.size,
                    updated=blob.updated.isoformat() if blob.updated else None,
                )
            )

    return ListPrefixResponse(objects=objects, prefixes=sorted(list(prefixes)))
