from storage_client import get_bucket
from storage_models import ObjectMetadataResponse, normalize_metadata


def object_metadata(bucket_name: str, object_name: str) -> ObjectMetadataResponse:
    bucket = get_bucket(bucket_name)
    blob = bucket.get_blob(object_name)
    if blob is None:
        raise FileNotFoundError(object_name)
    return ObjectMetadataResponse(bucket_name=bucket_name, object_name=object_name, size=blob.size, content_type=blob.content_type, metadata=normalize_metadata(getattr(blob, 'metadata', None)), etag=getattr(blob, 'etag', None), updated=getattr(blob, 'updated', None))
