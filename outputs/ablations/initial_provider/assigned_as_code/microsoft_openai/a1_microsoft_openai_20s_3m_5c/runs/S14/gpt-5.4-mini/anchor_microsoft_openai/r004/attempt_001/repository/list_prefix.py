from storage_client import get_blob_service_client, load_storage_config
from storage_models import normalize_list_item


def list_prefix(payload, config=None):
    resolved = load_storage_config(config)
    with get_blob_service_client(resolved) as client:
        container = client.get_container_client(resolved['container'])
        items = container.list_blobs(name_starts_with=payload.get('prefix', ''))
        return {'objects': [normalize_list_item(item) for item in items]}
