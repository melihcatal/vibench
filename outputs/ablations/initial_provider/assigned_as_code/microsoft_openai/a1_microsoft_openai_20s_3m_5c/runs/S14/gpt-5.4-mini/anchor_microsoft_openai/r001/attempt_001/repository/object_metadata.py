from storage_client import get_blob_service_client, load_storage_config
from storage_models import metadata_to_dict, normalize_object_name


def object_metadata(payload, config=None):
    config = load_storage_config(config)
    with get_blob_service_client(config) as client:
        blob = client.get_blob_client(container=config['container'], blob=normalize_object_name(payload['object_name']))
        props = blob.get_blob_properties()
    return metadata_to_dict(props.metadata, payload['object_name']) | {'content_type': props.content_settings.content_type, 'size': props.size}
