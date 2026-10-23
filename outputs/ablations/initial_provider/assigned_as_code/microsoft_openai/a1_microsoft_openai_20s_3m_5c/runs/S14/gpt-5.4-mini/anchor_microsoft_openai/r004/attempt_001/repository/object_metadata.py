from storage_client import get_blob_service_client, load_storage_config


def object_metadata(payload, config=None):
    resolved = load_storage_config(config)
    with get_blob_service_client(resolved) as client:
        blob = client.get_blob_client(container=resolved['container'], blob=payload['object_name'])
        props = blob.get_blob_properties()
    return {'object_name': payload['object_name'], 'content_type': props.content_settings.content_type, 'content_length': props.size, 'etag': props.etag}
