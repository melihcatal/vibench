from typing import Optional

from botocore.exceptions import ClientError

from storage_client import get_s3_client, handle_aws_error, normalize_metadata_response
from storage_models import StorageConfig, MetadataRequest, ObjectMetadata


def get_object_metadata(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    config: Optional[StorageConfig] = None,
) -> ObjectMetadata:
    s3_client = get_s3_client(config)

    head_kwargs = {"Bucket": bucket, "Key": key}
    if version_id:
        head_kwargs["VersionId"] = version_id

    try:
        response = s3_client.head_object(**head_kwargs)

        normalized = normalize_metadata_response(response, bucket, key)

        return ObjectMetadata(
            key=key,
            bucket=bucket,
            content_type=normalized["content_type"],
            content_length=normalized["content_length"],
            last_modified=normalized["last_modified"],
            etag=normalized["etag"],
            version_id=normalized["version_id"],
            storage_class=normalized["storage_class"],
            metadata=normalized["metadata"],
            exists=True,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            return ObjectMetadata(
                key=key,
                bucket=bucket,
                exists=False,
            )
        return ObjectMetadata(
            key=key,
            bucket=bucket,
            exists=False,
            error=handle_aws_error(e, "object_metadata"),
        )
    except Exception as e:
        return ObjectMetadata(
            key=key,
            bucket=bucket,
            exists=False,
            error=f"object_metadata error: {str(e)}",
        )


def get_object_metadata_from_request(
    request: MetadataRequest,
    config: Optional[StorageConfig] = None,
) -> ObjectMetadata:
    return get_object_metadata(
        bucket=request.bucket,
        key=request.key,
        version_id=request.version_id,
        config=config,
    )
