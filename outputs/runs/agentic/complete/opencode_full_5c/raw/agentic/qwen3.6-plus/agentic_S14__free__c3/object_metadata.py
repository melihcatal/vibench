from botocore.exceptions import ClientError

from storage_client import get_s3_client, validate_bucket_name
from storage_models import (
    MetadataRequest,
    MetadataResponse,
    normalize_s3_metadata,
    parse_s3_datetime,
)


def get_object_metadata(request: MetadataRequest) -> MetadataResponse:
    s3_client = get_s3_client()
    validate_bucket_name(request.bucket)

    head_kwargs = {
        "Bucket": request.bucket,
        "Key": request.key,
    }

    if request.version_id:
        head_kwargs["VersionId"] = request.version_id

    try:
        response = s3_client.head_object(**head_kwargs)

        return MetadataResponse(
            success=True,
            content_type=response.get("ContentType"),
            content_length=response.get("ContentLength"),
            last_modified=parse_s3_datetime(response.get("LastModified")),
            etag=response.get("ETag", "").strip('"'),
            storage_class=response.get("StorageClass"),
            metadata=normalize_s3_metadata(response.get("Metadata")),
            version_id=response.get("VersionId"),
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404" or error_code == "NoSuchKey":
            return MetadataResponse(
                success=False,
                error=f"Object not found: {request.bucket}/{request.key}",
            )
        return MetadataResponse(
            success=False,
            error=f"AWS S3 head_object failed: {error_code} - {e.response['Error']['Message']}",
        )
    except Exception as e:
        return MetadataResponse(
            success=False,
            error=str(e),
        )
