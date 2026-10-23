from storage_client import get_s3_client
from storage_models import MetadataResult


def read_object_metadata(bucket: str, key: str) -> MetadataResult:
    client = get_s3_client()
    head = client.head_object(Bucket=bucket, Key=key)
    return MetadataResult.from_head(bucket=bucket, key=key, head=head)
