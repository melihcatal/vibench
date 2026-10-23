from storage_client import get_s3_client
from storage_models import HeadObjectRequest, ObjectMetadata, normalize_head_object


def get_object_metadata(bucket: str, key: str, s3_client=None) -> ObjectMetadata:
    client = s3_client or get_s3_client()
    request = HeadObjectRequest(bucket=bucket, key=key)
    response = client.head_object(Bucket=request.bucket, Key=request.key)
    return ObjectMetadata(**normalize_head_object(response, request.bucket, request.key))
