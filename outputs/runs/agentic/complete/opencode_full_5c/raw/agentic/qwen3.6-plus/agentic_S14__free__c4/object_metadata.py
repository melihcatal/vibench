from datetime import datetime, timezone
from typing import Optional
from storage_client import get_s3_client, validate_bucket_name, validate_object_key
from storage_models import MetadataRequest, MetadataResponse


def get_object_metadata(request: MetadataRequest) -> MetadataResponse:
    if not validate_bucket_name(request.bucket):
        return MetadataResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=f"Invalid bucket name: {request.bucket}",
        )

    if not validate_object_key(request.key):
        return MetadataResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=f"Invalid object key: {request.key}",
        )

    s3_client = get_s3_client()

    head_kwargs = {
        "Bucket": request.bucket,
        "Key": request.key,
    }

    if request.version_id:
        head_kwargs["VersionId"] = request.version_id

    try:
        response = s3_client.head_object(**head_kwargs)

        metadata = {}
        if "Metadata" in response:
            metadata = response["Metadata"]

        last_modified = response.get("LastModified")
        if last_modified and isinstance(last_modified, datetime):
            if last_modified.tzinfo is None:
                last_modified = last_modified.replace(tzinfo=timezone.utc)

        return MetadataResponse(
            success=True,
            bucket=request.bucket,
            key=request.key,
            content_type=response.get("ContentType"),
            content_length=response.get("ContentLength", 0),
            last_modified=last_modified,
            etag=response.get("ETag", "").strip('"'),
            storage_class=response.get("StorageClass"),
            metadata=metadata,
            version_id=response.get("VersionId"),
            server_side_encryption=response.get("ServerSideEncryption"),
        )
    except s3_client.exceptions.ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        if error_code == "404":
            return MetadataResponse(
                success=False,
                bucket=request.bucket,
                key=request.key,
                error_message=f"Object not found: {request.key}",
            )
        return MetadataResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=str(e),
        )
    except Exception as e:
        return MetadataResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=str(e),
        )


def head_object(
    bucket: str, key: str, version_id: Optional[str] = None
) -> MetadataResponse:
    request = MetadataRequest(bucket=bucket, key=key, version_id=version_id)
    return get_object_metadata(request)
