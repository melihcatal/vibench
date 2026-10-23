from storage_client import get_bucket
from storage_models import ListPrefixResponse, ListedObject, normalize_metadata


def list_prefix(bucket_name: str, prefix: str = '') -> ListPrefixResponse:
    bucket = get_bucket(bucket_name)
    items = []
    for blob in bucket.list_blobs(prefix=prefix):
        items.append(ListedObject(name=blob.name, size=blob.size, content_type=blob.content_type, metadata=normalize_metadata(getattr(blob, 'metadata', None))))
    return ListPrefixResponse(bucket_name=bucket_name, prefix=prefix, objects=items)
