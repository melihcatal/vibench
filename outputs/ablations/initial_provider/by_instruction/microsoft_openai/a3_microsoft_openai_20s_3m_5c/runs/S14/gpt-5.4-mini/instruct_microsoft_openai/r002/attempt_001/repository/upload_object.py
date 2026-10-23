import io
from typing import Any, Optional

from azure.storage.blob import ContentSettings

from storage_client import get_blob_service_client, load_config, normalize_blob_name
from storage_models import UploadResult, normalize_payload


def upload_object(blob_name: str, data: Any, content_type: Optional[str] = None, container: Optional[str] = None) -> UploadResult:
    config = load_config(container)
    client = get_blob_service_client(config)
    blob_client = client.get_blob_client(container=config.container, blob=normalize_blob_name(blob_name))
    payload = normalize_payload(data)
    stream = io.BytesIO(payload)
    kwargs = {}
    if content_type:
        kwargs["content_settings"] = ContentSettings(content_type=content_type)
    response = blob_client.upload_blob(stream, overwrite=True, **kwargs)
    return UploadResult(container=config.container, blob=normalize_blob_name(blob_name), etag=getattr(response, "etag", None), url=blob_client.url)


def main() -> None:
    raise SystemExit("Provide blob_name and data to upload_object")
