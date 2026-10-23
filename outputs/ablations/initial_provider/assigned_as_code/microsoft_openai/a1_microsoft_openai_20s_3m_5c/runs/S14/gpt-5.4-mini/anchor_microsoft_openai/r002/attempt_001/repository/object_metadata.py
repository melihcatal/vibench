from storage_client import get_blob_service_client, normalize_blob_properties


def object_metadata(payload, config=None):
    with get_blob_service_client(config) as client:
        blob = client.get_blob_client(container=config['container'], blob=payload['object_name'])
        props = blob.get_blob_properties()
    return normalize_blob_properties(props)
