from botocore.exceptions import BotoCoreError, ClientError

from storage_client import get_s3_client, resolve_bucket_name, resolve_object_key
from storage_models import ObjectMetadataResponse, normalize_metadata


def get_object_metadata(bucket: str, key: str) -> ObjectMetadataResponse:
    client = get_s3_client()
    bucket_name = resolve_bucket_name(bucket)
    object_key = resolve_object_key(key)
    try:
        result = client.head_object(Bucket=bucket_name, Key=object_key)
        return ObjectMetadataResponse.from_head_object(bucket_name, object_key, normalize_metadata(result))
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"failed to read metadata for s3://{bucket_name}/{object_key}: {exc}") from exc


__all__ = ["get_object_metadata"]
