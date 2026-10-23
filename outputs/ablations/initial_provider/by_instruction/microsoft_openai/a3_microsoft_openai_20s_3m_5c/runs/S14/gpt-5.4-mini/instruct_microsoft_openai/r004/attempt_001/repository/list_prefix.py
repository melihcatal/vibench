from storage_client import get_container_client
from storage_models import StorageListRequest, normalize_prefix


def list_prefix(bucket: str, prefix: str = ""):
    request = StorageListRequest(bucket=bucket, prefix=normalize_prefix(prefix))
    container = get_container_client(request.bucket)
    return [blob.name for blob in container.list_blobs(name_starts_with=request.prefix)]
