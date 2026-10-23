import oss2
from storage_client import get_oss_bucket, normalize_object_key
from storage_models import (
    ObjectMetadataRequest,
    ObjectMetadataResponse,
    normalize_oss_metadata_to_response,
)


def get_object_metadata(
    bucket_name: str,
    object_key: str,
) -> ObjectMetadataResponse:
    object_key = normalize_object_key(object_key)
    bucket = get_oss_bucket(bucket_name)

    try:
        head_result = bucket.get_object_meta(object_key)
        head_result.key = object_key
        head_result.bucket_name = bucket_name
        return normalize_oss_metadata_to_response(head_result)
    except oss2.exceptions.NoSuchKey:
        return ObjectMetadataResponse(
            success=False,
            object_key=object_key,
            bucket=bucket_name,
            error="Object not found",
        )
    except oss2.exceptions.OssError as e:
        return ObjectMetadataResponse(
            success=False,
            object_key=object_key,
            bucket=bucket_name,
            error=str(e),
        )


def fetch_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    return get_object_metadata(
        bucket_name=request.bucket,
        object_key=request.object_key,
    )
