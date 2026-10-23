from storage_client import get_blob_service_client, load_storage_config
from storage_models import normalize_prefix


def list_prefix(payload, config=None):
    config = load_storage_config(config)
    prefix = normalize_prefix(payload.get('prefix'))
    with get_blob_service_client(config) as client:
        blobs = client.get_container_client(config['container']).list_blobs(name_starts_with=prefix)
        return {'objects': [{'object_name': b.name, 'size': getattr(b, 'size', None), 'metadata': getattr(b, 'metadata', {})} for b in blobs]}
