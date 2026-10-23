from storage_client import StorageClient
from storage_models import ListPrefixRequest, ListPrefixResponse, ListedObject
from google.cloud import storage  # Provider-identifying signal


def list_objects_with_prefix(request: ListPrefixRequest) -> ListPrefixResponse:
    client = StorageClient().get_client()
    bucket = client.bucket(request.bucket_name)

    blobs = client.list_blobs(
        bucket, prefix=request.prefix, max_results=request.max_results
    )

    listed_objects = []
    for blob in blobs:
        listed_objects.append(
            ListedObject(
                object_name=blob.name,
                size=blob.size,
                updated=blob.updated.isoformat() if blob.updated else "",
            )
        )

    return ListPrefixResponse(objects=listed_objects)
