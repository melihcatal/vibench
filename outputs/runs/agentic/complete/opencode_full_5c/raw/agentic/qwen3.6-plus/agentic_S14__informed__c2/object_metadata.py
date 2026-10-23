from typing import Optional

from botocore.exceptions import ClientError

from storage_client import StorageClient
from storage_models import ObjectMetadata


def get_object_metadata(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    version_id: Optional[str] = None,
    part_number: Optional[int] = None,
) -> ObjectMetadata:
    if not key:
        raise ValueError("key is required to retrieve object metadata")

    client = StorageClient()
    target_bucket = bucket or client.default_bucket
    if not target_bucket:
        raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

    head_kwargs = {
        "Bucket": target_bucket,
        "Key": key,
    }

    if version_id:
        head_kwargs["VersionId"] = version_id

    if part_number is not None:
        head_kwargs["PartNumber"] = part_number

    try:
        response = client.s3_client.head_object(**head_kwargs)
        return ObjectMetadata.from_s3_head(target_bucket, key, response)

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            raise FileNotFoundError(
                f"Object not found in Amazon S3: s3://{target_bucket}/{key}"
            ) from e
        error_message = e.response["Error"]["Message"]
        raise RuntimeError(
            f"Amazon S3 head_object failed for s3://{target_bucket}/{key}: "
            f"[{error_code}] {error_message}"
        ) from e


def object_exists(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    version_id: Optional[str] = None,
) -> bool:
    if not key:
        raise ValueError("key is required to check object existence")

    client = StorageClient()
    target_bucket = bucket or client.default_bucket
    if not target_bucket:
        raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

    head_kwargs = {
        "Bucket": target_bucket,
        "Key": key,
    }

    if version_id:
        head_kwargs["VersionId"] = version_id

    try:
        client.s3_client.head_object(**head_kwargs)
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code in ("404", "403"):
            return False
        raise


def get_object_size(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    version_id: Optional[str] = None,
) -> int:
    metadata = get_object_metadata(bucket, key, version_id)
    return metadata.content_length
