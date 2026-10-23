from storage_client import get_blob_service_client
from storage_models import normalize_listing


def list_prefix(payload, config=None):
    with get_blob_service_client(config) as client:
        items = client.get_container_client(config['container']).list_blobs(name_starts_with=payload.get('prefix', ''))
        return {'items': normalize_listing(items)}
