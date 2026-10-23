from storage_client import get_s3_client
from storage_models import MetadataResponse, StorageObjectRef, normalize_head_response


def object_metadata(ref: StorageObjectRef) -> MetadataResponse:
    client = get_s3_client()
    head = client.head_object(Bucket=ref.bucket, Key=ref.key)
    return normalize_head_response(ref.bucket, ref.key, head)
