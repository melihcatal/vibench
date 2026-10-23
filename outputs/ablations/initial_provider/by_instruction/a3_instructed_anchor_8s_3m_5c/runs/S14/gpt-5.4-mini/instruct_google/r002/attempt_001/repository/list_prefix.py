from storage_client import get_storage_client
from storage_models import ListPrefixRequest


def list_prefix(request: ListPrefixRequest) -> list:
    client = get_storage_client()
    blobs = client.list_blobs(request.bucket, prefix=request.prefix)
    return [
        {
            "bucket": request.bucket,
            "name": blob.name,
            "size": blob.size,
            "content_type": blob.content_type,
            "updated": blob.updated.isoformat() if blob.updated else None,
        }
        for blob in blobs
    ]
