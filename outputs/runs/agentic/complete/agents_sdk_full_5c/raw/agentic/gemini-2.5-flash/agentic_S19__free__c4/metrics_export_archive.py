from observability_client import get_storage_client
from observability_models import ArchiveResult
import os

def archive_metric_snapshot(bucket_name: str, blob_name: str, data: str) -> ArchiveResult:
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    try:
        blob.upload_from_string(data)
        return ArchiveResult(
            blob_name=blob_name,
            bucket_name=bucket_name,
            success=True,
            error_message=None
        )
    except Exception as e:
        return ArchiveResult(
            blob_name=blob_name,
            bucket_name=bucket_name,
            success=False,
            error_message=str(e)
        )
