from storage_client import get_s3_client, get_storage_config
from storage_models import ObjectMetadataRequest, ObjectMetadataResponse, normalize_metadata_response


def read_object_metadata(request: ObjectMetadataRequest) -> ObjectMetadataResponse:
    config = get_storage_config()
    client = get_s3_client(config)
    head = client.head_object(Bucket=request.bucket, Key=request.key)
    return normalize_metadata_response(request.bucket, request.key, head)
