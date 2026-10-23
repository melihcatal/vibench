from storage_client import get_s3_client, load_storage_config
from storage_models import metadata_from_head_response, normalize_object_name


def object_metadata(payload, config=None):
    config = load_storage_config(config)
    client = get_s3_client(config)
    head = client.head_object(Bucket=config["bucket"], Key=normalize_object_name(payload["object_name"]))
    return metadata_from_head_response(head)
