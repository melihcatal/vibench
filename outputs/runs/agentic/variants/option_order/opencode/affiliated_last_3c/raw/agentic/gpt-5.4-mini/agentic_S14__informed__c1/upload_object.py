import io
from typing import BinaryIO, Optional, Union

from google.cloud import storage

from storage_client import get_bucket, get_storage_client, load_storage_config
from storage_models import normalize_object_name, metadata_to_dict


def upload_object(
    object_name: str,
    data: Union[bytes, bytearray, BinaryIO],
    content_type: Optional[str] = None,
):
    config = load_storage_config()
    client: storage.Client = get_storage_client()
    bucket = get_bucket(client, config.bucket_name)
    object_name = normalize_object_name(object_name)
    blob = bucket.blob(object_name)
    if isinstance(data, (bytes, bytearray)):
        blob.upload_from_string(bytes(data), content_type=content_type)
    else:
        blob.upload_from_file(data, content_type=content_type)
    blob.reload()
    return metadata_to_dict(__import__("storage_models").metadata_from_blob(blob))


def upload_bytes(object_name: str, payload: bytes, content_type: Optional[str] = None):
    return upload_object(object_name, payload, content_type=content_type)


def upload_stream(
    object_name: str, stream: BinaryIO, content_type: Optional[str] = None
):
    return upload_object(object_name, stream, content_type=content_type)
