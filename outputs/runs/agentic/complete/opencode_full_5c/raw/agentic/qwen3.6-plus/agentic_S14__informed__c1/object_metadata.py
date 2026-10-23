from datetime import datetime

from storage_client import get_s3_client, validate_bucket_name, validate_object_key
from storage_models import MetadataRequest, ObjectMetadata


def get_object_metadata(
    bucket: str,
    key: str,
    version_id: str = None,
) -> ObjectMetadata:
    client = get_s3_client()
    validate_bucket_name(bucket)
    validate_object_key(key)

    params = {
        "Bucket": bucket,
        "Key": key,
    }

    if version_id:
        params["VersionId"] = version_id

    try:
        response = client.head_object(**params)

        metadata = {}
        for mk, mv in response.get("Metadata", {}).items():
            metadata[mk] = mv

        last_modified = response.get("LastModified")
        if last_modified and isinstance(last_modified, datetime):
            pass
        elif last_modified:
            last_modified = datetime.fromisoformat(last_modified.replace("Z", "+00:00"))

        return ObjectMetadata(
            bucket=bucket,
            key=key,
            content_type=response.get("ContentType"),
            content_length=response.get("ContentLength", 0),
            etag=response.get("ETag", "").strip('"'),
            last_modified=last_modified,
            storage_class=response.get("StorageClass"),
            version_id=response.get("VersionId"),
            metadata=metadata,
            delete_marker=response.get("DeleteMarker", False),
        )

    except Exception as exc:
        return ObjectMetadata(
            bucket=bucket,
            key=key,
            metadata={},
        )


def get_metadata_from_request(request: MetadataRequest) -> ObjectMetadata:
    return get_object_metadata(
        bucket=request.bucket,
        key=request.key,
        version_id=request.version_id,
    )
