from storage_client import get_s3_client
from storage_models import ListPrefixResult


def list_objects_with_prefix(bucket: str, prefix: str = '') -> ListPrefixResult:
    client = get_s3_client()
    response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return ListPrefixResult.from_list_response(bucket=bucket, prefix=prefix, response=response)
