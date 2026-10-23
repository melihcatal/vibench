from storage_client import get_s3_client, raise_storage_error
from storage_models import ObjectMetadata, normalize_mapping, isoformat, to_dict


def object_metadata(bucket: str, key: str):
    try:
        response = get_s3_client().head_object(Bucket=bucket, Key=key)
        result = ObjectMetadata(
            bucket=bucket,
            key=key,
            etag=response.get("ETag"),
            size=response.get("ContentLength"),
            last_modified=isoformat(response.get("LastModified")),
            content_type=response.get("ContentType"),
            metadata=normalize_mapping(response.get("Metadata")),
        )
        return to_dict(result)
    except Exception as exc:
        raise raise_storage_error(exc)
