from typing import Optional
from b2sdk.v2 import B2Api
from storage_client import get_b2_client, get_bucket_name
from storage_models import ListPrefixResponse, StorageObject


def list_prefix(prefix: str, delimiter: Optional[str] = None, max_keys: int = 1000) -> ListPrefixResponse:
    b2_api: B2Api = get_b2_client()
    bucket = b2_api.get_bucket_by_name(get_bucket_name())

    file_versions = bucket.ls(prefix, delimiter=delimiter, latest_only=True, fetch_count=max_keys)
    objects = []
    
    for file_version, _ in file_versions:
        objects.append(
            StorageObject(
                name=file_version.file_name,
                size=file_version.content_length,
                content_type=file_version.content_type,
                last_modified=file_version.upload_timestamp / 1000,
                metadata=file_version.file_info
            )
        )

    return ListPrefixResponse(objects=objects)