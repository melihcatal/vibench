from storage_client import build_blob_service_client


def list_prefix(payload, config=None):
    config = config or {}
    client = build_blob_service_client(config)
    blobs = client.get_container_client(config['container']).list_blobs(name_starts_with=payload.get('prefix', ''))
    return {'objects': [{'object_name': item.name, 'size': item.size, 'etag': item.etag} for item in blobs]}
