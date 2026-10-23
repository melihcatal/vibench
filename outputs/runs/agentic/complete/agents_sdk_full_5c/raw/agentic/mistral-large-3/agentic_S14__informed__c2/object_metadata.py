from typing import Dict
from b2sdk.v2 import B2Api
from storage_client import get_b2_client, get_bucket_name
from storage_models import StorageObject


def get_object_metadata(object_name: str) -> StorageObject:
    b2_api: B2Api = get_b2_client()
    bucket = b2_api.get_bucket_by_name(get_bucket_name())

    b2_file = bucket.get_file_info_by_name(object_name)
    
    return StorageObject(
        name=b2_file.file_name,
        size=b2_file.content_length,
        content_type=b2_file.content_type,
        last_modified=b2_file.upload_timestamp / 1000,  # Convert from millis
        metadata=b2_file.file_info
    )