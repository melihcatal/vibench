from storage_client import get_blob_service_client


def object_metadata(payload, config=None):
    config = config or {}
    account_url = config['account_url']
    container_name = config['container']
    object_name = payload['object_name']

    client = get_blob_service_client(account_url)
    blob_client = client.get_blob_client(container=container_name, blob=object_name)

    properties = blob_client.get_blob_properties()

    return {
        'object_name': object_name,
        'size': properties.size,
        'creation_time': properties.creation_time.isoformat(),
        'last_modified': properties.last_modified.isoformat(),
        'content_type': properties.content_settings.content_type,
        'metadata': properties.metadata
    }
