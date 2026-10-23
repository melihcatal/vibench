from storage_client import get_s3_client
from storage_models import ObjectMetadataResult


def get_object_metadata(bucket_name: str, object_name: str, config: dict = None) -> ObjectMetadataResult:
    config = config or {}
    s3_client = get_s3_client(region_name=config.get("region"))
    response = s3_client.head_object(Bucket=bucket_name, Key=object_name)
    return ObjectMetadataResult(metadata=response)
