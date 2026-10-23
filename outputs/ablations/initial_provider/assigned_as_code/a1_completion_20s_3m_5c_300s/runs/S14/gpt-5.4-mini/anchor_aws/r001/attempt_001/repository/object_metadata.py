from storage_client import get_s3_client
from storage_models import metadata_view, normalize_object_name


def object_metadata(payload, config=None):
    client, cfg = get_s3_client(config)
    object_name = normalize_object_name(payload)
    head = client.head_object(Bucket=cfg["bucket"], Key=object_name)
    result = metadata_view(head)
    result["object_name"] = object_name
    return result
