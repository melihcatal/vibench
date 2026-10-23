from storage_client import get_blob_service_client


def list_prefix(payload, config=None):
    config = config or {}
    account_url = config['account_url']
    container_name = config['container']
    prefix = payload.get('prefix', '')

    client = get_blob_service_client(account_url)
    container_client = client.get_container_client(container_name)

    blobs = []
    for blob in container_client.list_blobs(name_starts_with=prefix):
        blobs.append({
            'object_name': blob.name,
            'size': blob.size,
            'creation_time': blob.creation_time.isoformat(),
            'last_modified': blob.last_modified.isoformat(),
            'content_type': blob.content_settings.content_type,
        })

    return {'prefix': prefix, 'objects': blobs}
