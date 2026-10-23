from storage_client import get_bucket_name, get_s3_client, load_storage_config
from storage_models import normalize_object_name


def object_metadata(payload, config=None):
    config = load_storage_config(config)
    client = get_s3_client(config)
    response = client.head_object(Bucket=get_bucket_name(config), Key=normalize_object_name(payload["object_name"]))
    return {"metadata": response.get("Metadata", {}), "content_type": response.get("ContentType"), "content_length": response.get("ContentLength"), "etag": response.get("ETag")}
