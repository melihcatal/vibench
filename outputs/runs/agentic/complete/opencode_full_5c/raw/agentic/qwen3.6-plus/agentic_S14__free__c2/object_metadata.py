from storage_client import get_s3_client, validate_bucket_name, handle_s3_error
from storage_models import MetadataRequest, ObjectMetadata, normalize_object_metadata


def get_object_metadata(
    bucket: str,
    key: str,
    version_id: str = None,
    region_name: str = None,
) -> ObjectMetadata:
    validate_bucket_name(bucket)
    s3 = get_s3_client(region_name=region_name)
    params = {
        "Bucket": bucket,
        "Key": key,
    }
    if version_id:
        params["VersionId"] = version_id
    try:
        response = s3.head_object(**params)
        return normalize_object_metadata(response, bucket, key)
    except Exception as exc:
        handle_s3_error(exc, "head_object", bucket, key)


def fetch_metadata(request: MetadataRequest, region_name: str = None) -> ObjectMetadata:
    return get_object_metadata(
        bucket=request.bucket,
        key=request.key,
        version_id=request.version_id,
        region_name=region_name,
    )
