from storage_client import get_blob_client
from storage_models import StoredObjectMetadata


def object_metadata(payload, config=None):
    blob = get_blob_client(config, payload['object_name'])
    props = blob.get_blob_properties()
    return StoredObjectMetadata(
        object_name=payload['object_name'],
        container=(config or {})['container'],
        size=props.size,
        content_type=props.content_settings.content_type if props.content_settings else None,
        etag=props.etag,
        last_modified=props.last_modified.isoformat() if props.last_modified else None,
        metadata=dict(props.metadata or {}),
    ).__dict__
