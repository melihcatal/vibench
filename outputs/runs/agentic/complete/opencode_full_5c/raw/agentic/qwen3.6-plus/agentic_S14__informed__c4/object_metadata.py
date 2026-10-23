from datetime import datetime, timezone
from typing import Optional

from storage_client import get_s3_client, get_bucket_name
from storage_models import MetadataRequest, MetadataResponse


def object_metadata(
    key: str,
    bucket: Optional[str] = None,
) -> MetadataResponse:
    if bucket is None:
        bucket = get_bucket_name()

    s3_client = get_s3_client()

    try:
        response = s3_client.head_object(Bucket=bucket, Key=key)

        metadata = {}
        for mk, mv in response.get("Metadata", {}).items():
            metadata[mk.lower()] = mv

        last_modified = response.get("LastModified")
        if last_modified:
            if hasattr(last_modified, "astimezone"):
                last_modified = last_modified.astimezone(timezone.utc)
            else:
                last_modified = datetime.fromtimestamp(last_modified, tz=timezone.utc)

        return MetadataResponse(
            success=True,
            content_type=response.get("ContentType"),
            content_length=response.get("ContentLength"),
            etag=response.get("ETag", "").strip('"'),
            last_modified=last_modified,
            storage_class=response.get("StorageClass", "STANDARD"),
            metadata=metadata,
            version_id=response.get("VersionId"),
        )
    except Exception as exc:
        return MetadataResponse(
            success=False,
            error=str(exc),
        )
