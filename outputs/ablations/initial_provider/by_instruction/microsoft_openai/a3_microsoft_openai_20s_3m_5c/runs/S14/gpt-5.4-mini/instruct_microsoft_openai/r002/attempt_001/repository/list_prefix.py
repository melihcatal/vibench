from storage_client import get_blob_service_client, load_config
from storage_models import ListingResult, normalize_list_items


def list_prefix(prefix: str = "", container: str = None) -> ListingResult:
    config = load_config(container)
    client = get_blob_service_client(config)
    blobs = client.get_container_client(config.container).list_blobs(name_starts_with=prefix)
    return ListingResult(container=config.container, prefix=prefix, objects=normalize_list_items(blobs))
